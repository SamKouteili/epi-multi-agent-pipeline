"""Stage 1: Deep research via Perplexity Sonar Deep Research API."""

import logging

from openai import OpenAI

from src.config import PERPLEXITY_API_KEY, PERPLEXITY_MODEL, PERPLEXITY_TIMEOUT, OUTPUTS_DIR
from src.domain_knowledge import DOMAIN_KNOWLEDGE
from src.stage1.prompts import RESEARCH_PROMPT_TEMPLATE

logger = logging.getLogger(__name__)


def run_deep_research(tla: str, metadata: dict) -> tuple[str, list[str]]:
    """Run Perplexity deep research for a given EPI indicator.

    Args:
        tla: Three-letter abbreviation of the EPI indicator.
        metadata: Indicator metadata dict from master_variable_list.csv.

    Returns:
        Tuple of (markdown report, list of citation strings).
    """
    client = OpenAI(
        api_key=PERPLEXITY_API_KEY,
        base_url="https://api.perplexity.ai",
    )

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

    logger.info("Sending deep research request to Perplexity for %s...", tla)

    response = client.chat.completions.create(
        model=PERPLEXITY_MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a research assistant specializing in environmental data, "
                    "public health statistics, and cross-country empirical analysis. "
                    "Be thorough, cite specific datasets and papers, and include URLs."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        timeout=PERPLEXITY_TIMEOUT,
    )

    markdown = response.choices[0].message.content or ""
    citations = []
    if hasattr(response, "citations") and response.citations:
        citations = list(response.citations)

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
