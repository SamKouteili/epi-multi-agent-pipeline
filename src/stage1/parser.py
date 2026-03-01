"""Stage 1: Parse research report into structured hypotheses using Claude."""

import json
import logging

import anthropic

from src.config import ANTHROPIC_API_KEY, CLAUDE_PARSING_MODEL, OUTPUTS_DIR
from src.schemas import ProxyHypothesis, ResearchOutput
from src.stage1.prompts import PARSE_PROMPT_TEMPLATE

logger = logging.getLogger(__name__)


def parse_research_report(
    tla: str,
    markdown: str,
    citations: list[str],
    metadata: dict,
) -> ResearchOutput:
    """Parse a research markdown report into structured ProxyHypothesis objects.

    Args:
        tla: Three-letter abbreviation of the EPI indicator.
        markdown: Raw markdown report from Perplexity.
        citations: List of citation strings from the research.
        metadata: Indicator metadata dict.

    Returns:
        ResearchOutput with parsed hypotheses.
    """
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    prompt = PARSE_PROMPT_TEMPLATE.format(
        tla=tla,
        indicator_name=metadata.get("Description", tla),
        units=metadata.get("Units", "unknown"),
        source_org=metadata.get("Source", "unknown"),
        issue_category=metadata.get("IssueCategory", "unknown"),
        polarity=metadata.get("RawPolarity", "unknown"),
        report_markdown=markdown,
        citations="\n".join(f"[{i+1}] {c}" for i, c in enumerate(citations)) if citations else "None provided",
    )

    logger.info("Parsing research report for %s with Claude...", tla)

    response = client.messages.create(
        model=CLAUDE_PARSING_MODEL,
        max_tokens=8192,
        messages=[{"role": "user", "content": prompt}],
    )

    raw_text = response.content[0].text

    # Strip markdown fences if present
    if raw_text.startswith("```"):
        lines = raw_text.split("\n")
        # Remove first and last lines (fences)
        lines = lines[1:-1] if lines[-1].strip() == "```" else lines[1:]
        raw_text = "\n".join(lines)

    parsed = json.loads(raw_text)

    # Validate each hypothesis through Pydantic
    hypotheses = []
    for h_data in parsed.get("hypotheses", []):
        try:
            hypothesis = ProxyHypothesis.model_validate(h_data)
            hypotheses.append(hypothesis)
        except Exception as e:
            logger.warning("Failed to validate hypothesis %s: %s", h_data.get("id", "?"), e)

    causal_map = parsed.get("causal_map_summary", "")

    # Save parsed output
    output_dir = OUTPUTS_DIR / tla / "stage1"
    output_dir.mkdir(parents=True, exist_ok=True)
    hypotheses_path = output_dir / "hypotheses.json"
    output_data = {
        "indicator_tla": tla,
        "causal_map_summary": causal_map,
        "hypotheses": [h.model_dump() for h in hypotheses],
    }
    hypotheses_path.write_text(json.dumps(output_data, indent=2), encoding="utf-8")
    logger.info("Saved %d hypotheses to %s", len(hypotheses), hypotheses_path)

    return ResearchOutput(
        indicator_tla=tla,
        hypotheses=hypotheses,
        causal_map_summary=causal_map,
        raw_report_path=str(OUTPUTS_DIR / tla / "stage1" / "research_report.md"),
    )
