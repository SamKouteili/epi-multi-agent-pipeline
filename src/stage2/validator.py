"""Post-verification validation agent: reviews verification outputs for quality issues."""

import json
import logging
from pathlib import Path
from typing import Optional

import anthropic

from src.config import ANTHROPIC_API_KEY, CLAUDE_VALIDATION_MODEL, VALIDATION_MAX_TOKENS
from src.schemas import ProxyHypothesis, ValidationAnnotation, VerificationResult
from src.stage2.prompts import VALIDATOR_SYSTEM_PROMPT, build_validation_prompt

logger = logging.getLogger(__name__)


def _read_file_safe(path: Path) -> str:
    """Read a file, returning empty string if missing or unreadable."""
    try:
        return path.read_text(encoding="utf-8")
    except (FileNotFoundError, OSError) as e:
        logger.debug("Could not read %s: %s", path, e)
        return ""


def _strip_markdown_fences(text: str) -> str:
    """Strip markdown code fences if present (```json ... ```)."""
    text = text.strip()
    if text.startswith("```"):
        lines = text.split("\n")
        lines = lines[1:]  # remove opening fence
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]  # remove closing fence
        text = "\n".join(lines)
    return text


async def validate_result(
    hypothesis: ProxyHypothesis,
    verification_result: VerificationResult,
    output_dir: Path,
) -> Optional[ValidationAnnotation]:
    """Validate a verification result by reviewing the agent's outputs.

    Args:
        hypothesis: The proxy hypothesis that was verified.
        verification_result: The structured result from verification.
        output_dir: Directory containing verify.py, result.json, agent_output.txt.

    Returns:
        ValidationAnnotation if successful, None on failure.
    """
    # Read verification artifacts
    verify_py = _read_file_safe(output_dir / "verify.py")
    result_json = _read_file_safe(output_dir / "result.json")
    # Fall back to in-memory result if file not on disk
    if not result_json:
        result_json = verification_result.model_dump_json(indent=2)
    agent_output = _read_file_safe(output_dir / "agent_output.txt")

    if not verify_py and not result_json:
        logger.warning("No verify.py or result.json found in %s — skipping validation", output_dir)
        return None

    # Build prompt
    hypothesis_json = hypothesis.model_dump_json(indent=2)
    user_prompt = build_validation_prompt(
        hypothesis_json=hypothesis_json,
        verify_py_contents=verify_py,
        result_json_contents=result_json,
        agent_output_contents=agent_output,
    )

    # Call Anthropic API (async)
    client = anthropic.AsyncAnthropic(api_key=ANTHROPIC_API_KEY)

    logger.info("Validating %s with %s...", hypothesis.id, CLAUDE_VALIDATION_MODEL)

    response = await client.messages.create(
        model=CLAUDE_VALIDATION_MODEL,
        max_tokens=VALIDATION_MAX_TOKENS,
        system=VALIDATOR_SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_prompt}],
    )

    raw_text = response.content[0].text
    raw_text = _strip_markdown_fences(raw_text)

    # Parse and validate
    parsed = json.loads(raw_text)
    annotation = ValidationAnnotation.model_validate(parsed)

    # Save standalone validation.json
    validation_path = output_dir / "validation.json"
    validation_path.write_text(
        json.dumps(parsed, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    logger.info("Saved validation to %s", validation_path)

    return annotation
