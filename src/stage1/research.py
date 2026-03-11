"""Stage 1: Deep research via Gemini Deep Research API."""

import logging
import time

from google import genai

from src.config import (
    GEMINI_API_KEY,
    GEMINI_DEEP_RESEARCH_AGENT,
    DEEP_RESEARCH_POLL_INTERVAL,
    DEEP_RESEARCH_MAX_WAIT,
    OUTPUTS_DIR,
)
from src.domain_knowledge import DOMAIN_KNOWLEDGE
from src.stage1.prompts import RESEARCH_PROMPT_TEMPLATE

logger = logging.getLogger(__name__)


def run_deep_research(tla: str, metadata: dict) -> tuple[str, list[str]]:
    """Run Gemini deep research for a given EPI indicator.

    Args:
        tla: Three-letter abbreviation of the EPI indicator.
        metadata: Indicator metadata dict from master_variable_list.csv.

    Returns:
        Tuple of (markdown report, list of citation strings).
    """
    client = genai.Client(api_key=GEMINI_API_KEY)

    # Build the research prompt
    polarity = metadata.get("RawPolarity", "unknown")
    polarity_desc = "higher values = better" if polarity == "positive" else "higher values = worse"

    oldyear = metadata.get("Oldyear")
    if oldyear and str(oldyear) != "nan":
        year_range = f"{int(oldyear)}-2024"
    else:
        year_range = "varies"

    # Build domain knowledge section if available
    dk = DOMAIN_KNOWLEDGE.get(tla)
    if dk:
        domain_knowledge_section = (
            "## Domain Context (from EPI Technical Appendix)\n"
            "The following is known about this indicator from the EPI team's own analysis. "
            "Use this as a starting point — do NOT spend effort rediscovering these facts. "
            "Instead, focus on finding proxy sources BEYOND what is described here.\n\n"
            f"{dk}\n\n"
        )
    else:
        domain_knowledge_section = ""

    prompt = RESEARCH_PROMPT_TEMPLATE.format(
        tla=tla,
        indicator_name=metadata.get("Description", tla),
        units=metadata.get("Units", "unknown"),
        source_org=metadata.get("Source", "unknown"),
        issue_category=metadata.get("IssueCategory", "unknown"),
        polarity=polarity,
        polarity_description=polarity_desc,
        n_countries=180,
        year_range=year_range,
        domain_knowledge_section=domain_knowledge_section,
    )

    logger.info("Sending deep research request to Gemini for %s...", tla)

    # Launch the deep research task (runs asynchronously)
    interaction = client.interactions.create(
        input=prompt,
        agent=GEMINI_DEEP_RESEARCH_AGENT,
        background=True,
    )

    logger.info("Deep research task started (id=%s), polling for completion...", interaction.id)

    # Poll until complete
    elapsed = 0
    while elapsed < DEEP_RESEARCH_MAX_WAIT:
        time.sleep(DEEP_RESEARCH_POLL_INTERVAL)
        elapsed += DEEP_RESEARCH_POLL_INTERVAL
        interaction = client.interactions.get(interaction.id)

        if interaction.status == "completed":
            logger.info("Deep research completed after ~%ds", elapsed)
            break
        elif interaction.status == "failed":
            error_msg = getattr(interaction, "error", "unknown error")
            raise RuntimeError(f"Gemini deep research failed for {tla}: {error_msg}")

        if elapsed % 60 < DEEP_RESEARCH_POLL_INTERVAL:
            logger.info("Still researching %s... (%ds elapsed)", tla, elapsed)
    else:
        raise TimeoutError(
            f"Gemini deep research timed out after {DEEP_RESEARCH_MAX_WAIT}s for {tla}"
        )

    # Extract the final report text from the last output
    markdown = ""
    if interaction.outputs:
        markdown = interaction.outputs[-1].text or ""

    # Gemini deep research includes inline citations; extract source URLs if available
    citations = []
    if hasattr(interaction, "citations") and interaction.citations:
        citations = list(interaction.citations)
    # Also check outputs for grounding metadata
    if interaction.outputs:
        last_output = interaction.outputs[-1]
        if hasattr(last_output, "grounding_metadata") and last_output.grounding_metadata:
            gm = last_output.grounding_metadata
            if hasattr(gm, "grounding_chunks") and gm.grounding_chunks:
                for chunk in gm.grounding_chunks:
                    if hasattr(chunk, "web") and chunk.web:
                        url = getattr(chunk.web, "uri", None)
                        if url and url not in citations:
                            citations.append(url)

    # Save raw report with citation legend appended
    output_dir = OUTPUTS_DIR / tla / "stage1"
    output_dir.mkdir(parents=True, exist_ok=True)
    report_path = output_dir / "research_report.md"
    report_text = markdown
    if citations:
        legend = "\n\n## References\n" + "\n".join(
            f"[{i+1}] {url}" for i, url in enumerate(citations)
        )
        report_text += legend
    report_path.write_text(report_text, encoding="utf-8")
    logger.info("Research report saved to %s (%d chars, %d citations)", report_path, len(report_text), len(citations))

    return markdown, citations
