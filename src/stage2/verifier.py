"""Stage 2: Hypothesis verification using Anthropic API + subprocess."""

import json
import logging
import os
import re
import subprocess
import sys
from pathlib import Path

import anthropic

from src.config import PROJECT_ROOT, RAW_DIR, OUTPUTS_DIR, ANTHROPIC_API_KEY, CLAUDE_VERIFICATION_MODEL
from src.schemas import ProxyHypothesis, VerificationMethod, VerificationResult, Verdict
from src.stage2.prompts import VERIFIER_SYSTEM_PROMPT, build_verification_prompt
from src.stage2.data_loader import prepare_verification_context

logger = logging.getLogger(__name__)

MAX_RETRIES = 3
SCRIPT_TIMEOUT = 120  # seconds


def _extract_python_script(text: str) -> str:
    """Extract the Python script from Claude's response.

    Looks for a fenced code block first, then falls back to the entire text.
    """
    # Try to find a fenced python block
    pattern = r"```python\s*\n(.*?)```"
    match = re.search(pattern, text, re.DOTALL)
    if match:
        return match.group(1).strip()

    # Fallback: look for any fenced block
    pattern = r"```\s*\n(.*?)```"
    match = re.search(pattern, text, re.DOTALL)
    if match:
        return match.group(1).strip()

    # Last resort: return the whole text (it might be a raw script)
    return text.strip()


async def verify_hypothesis(
    hypothesis: ProxyHypothesis,
    tla: str,
    output_dir: Path | None = None,
    prompt_override: str | None = None,
) -> VerificationResult:
    """Verify a single proxy hypothesis using Claude API + subprocess.

    1. Ask Claude to generate a verify.py script
    2. Execute the script via subprocess
    3. If it fails, send the error back to Claude for a corrected script (up to 3 attempts)
    4. Parse result.json

    Args:
        hypothesis: The hypothesis to verify.
        tla: Target indicator TLA.
        output_dir: Override output directory (defaults to outputs/{TLA}/stage2/{HYP_ID}/).
        prompt_override: If provided, use this prompt instead of build_verification_prompt().

    Returns:
        VerificationResult parsed from the agent's output.
    """
    if output_dir is None:
        output_dir = OUTPUTS_DIR / tla / "stage2" / hypothesis.id

    output_dir.mkdir(parents=True, exist_ok=True)

    # Prepare context
    data_summary = prepare_verification_context(tla)
    system_prompt = VERIFIER_SYSTEM_PROMPT.format(raw_dir=RAW_DIR)
    verification_prompt = prompt_override or build_verification_prompt(hypothesis, tla, data_summary, output_dir)

    logger.info("Verifying hypothesis %s in %s", hypothesis.id, output_dir)

    client = anthropic.AsyncAnthropic(api_key=ANTHROPIC_API_KEY)

    script_path = output_dir / "verify.py"
    result_path = output_dir / "result.json"
    agent_log_path = output_dir / "agent_output.txt"

    # Conversation messages for retry loop
    messages = [{"role": "user", "content": verification_prompt}]
    agent_output_lines = []

    for attempt in range(1, MAX_RETRIES + 1):
        logger.info("Attempt %d/%d for %s", attempt, MAX_RETRIES, hypothesis.id)

        # Ask Claude to generate the script
        try:
            response = await client.messages.create(
                model=CLAUDE_VERIFICATION_MODEL,
                max_tokens=8192,
                system=system_prompt,
                messages=messages,
            )
            response_text = response.content[0].text
            agent_output_lines.append(f"=== Attempt {attempt} — Claude response ===")
            agent_output_lines.append(response_text)
        except Exception as e:
            logger.error("API call failed for %s (attempt %d): %s", hypothesis.id, attempt, e)
            agent_output_lines.append(f"=== Attempt {attempt} — API error: {e} ===")
            if attempt == MAX_RETRIES:
                break
            continue

        # Extract and write the script
        script_content = _extract_python_script(response_text)
        script_path.write_text(script_content, encoding="utf-8")
        logger.info("Wrote verify.py (%d chars) for %s", len(script_content), hypothesis.id)

        # Execute the script
        try:
            proc = subprocess.run(
                [sys.executable, str(script_path)],
                capture_output=True,
                text=True,
                timeout=SCRIPT_TIMEOUT,
                cwd=str(PROJECT_ROOT),
                env={
                    **os.environ,
                    "PYTHONDONTWRITEBYTECODE": "1",
                    "PYTHONPATH": str(PROJECT_ROOT),
                },
            )
            agent_output_lines.append(f"=== Attempt {attempt} — stdout ===")
            agent_output_lines.append(proc.stdout)
            agent_output_lines.append(f"=== Attempt {attempt} — stderr ===")
            agent_output_lines.append(proc.stderr)

            if proc.returncode == 0:
                logger.info("verify.py succeeded for %s", hypothesis.id)
                break
            else:
                error_msg = proc.stderr or proc.stdout or "(no output)"
                logger.warning(
                    "verify.py failed for %s (attempt %d, rc=%d): %s",
                    hypothesis.id, attempt, proc.returncode, error_msg[:500],
                )

                if attempt < MAX_RETRIES:
                    # Send error back to Claude for correction
                    messages.append({"role": "assistant", "content": response_text})
                    messages.append({
                        "role": "user",
                        "content": (
                            f"The script failed with return code {proc.returncode}.\n\n"
                            f"**stderr:**\n```\n{proc.stderr[:3000]}\n```\n\n"
                            f"**stdout:**\n```\n{proc.stdout[:2000]}\n```\n\n"
                            "Please fix the script and provide the COMPLETE corrected version. "
                            "Remember to use the shared library functions from src.utils.stats "
                            "and src.utils.data_utils."
                        ),
                    })

        except subprocess.TimeoutExpired:
            logger.warning("verify.py timed out for %s (attempt %d)", hypothesis.id, attempt)
            agent_output_lines.append(f"=== Attempt {attempt} — TIMEOUT ({SCRIPT_TIMEOUT}s) ===")
            if attempt < MAX_RETRIES:
                messages.append({"role": "assistant", "content": response_text})
                messages.append({
                    "role": "user",
                    "content": (
                        f"The script timed out after {SCRIPT_TIMEOUT} seconds. "
                        "This usually means an API call is hanging or there's an infinite loop. "
                        "Please fix and provide the COMPLETE corrected version."
                    ),
                })

    # Save agent output log
    agent_log_path.write_text("\n".join(agent_output_lines), encoding="utf-8")
    agent_tail = "\n".join(agent_output_lines[-5:]).strip() if agent_output_lines else ""

    # Fixup: check if result.json was written to PROJECT_ROOT instead of output_dir
    misplaced_path = PROJECT_ROOT / "result.json"
    if not result_path.exists() and misplaced_path.exists():
        logger.warning(
            "Fixup: result.json found at PROJECT_ROOT instead of %s — moving it",
            output_dir,
        )
        import shutil
        shutil.move(str(misplaced_path), str(result_path))

    # Parse result.json written by the script
    if result_path.exists():
        try:
            raw = json.loads(result_path.read_text(encoding="utf-8"))
            raw = _fixup_result_json(raw, hypothesis.id)
            return _parse_agent_result(hypothesis.id, raw, output_dir)
        except (json.JSONDecodeError, Exception) as e:
            logger.warning("Failed to parse result.json for %s: %s", hypothesis.id, e)
            return VerificationResult(
                hypothesis_id=hypothesis.id,
                verdict=Verdict.inconclusive,
                data_quality_notes=f"result.json parse error: {e}\n\nAgent output (last lines):\n{agent_tail}",
                script_path=str(script_path) if script_path.exists() else None,
                summary="Script completed but result.json could not be parsed.",
            )
    else:
        logger.warning("No result.json found for %s", hypothesis.id)
        return VerificationResult(
            hypothesis_id=hypothesis.id,
            verdict=Verdict.inconclusive,
            data_quality_notes=f"Script did not produce result.json\n\nAgent output (last lines):\n{agent_tail}",
            script_path=str(script_path) if script_path.exists() else None,
            summary="Verification incomplete — no result.json produced.",
        )


def _fixup_result_json(raw: dict, hypothesis_id: str) -> dict:
    """Apply common fixups to agent-produced result.json before parsing."""
    # Strip "Verdict." prefix from verdict values (e.g. "Verdict.confirmed" -> "confirmed")
    verdict = raw.get("verdict", "")
    if isinstance(verdict, str) and verdict.startswith("Verdict."):
        fixed = verdict.split(".", 1)[1]
        logger.warning(
            "Fixup %s: stripped Verdict prefix: %r -> %r", hypothesis_id, verdict, fixed
        )
        raw["verdict"] = fixed

    # Normalize uppercase verdict values (e.g. "CONFIRMED" -> "confirmed")
    if isinstance(raw.get("verdict"), str):
        raw["verdict"] = raw["verdict"].lower()

    return raw


def _parse_agent_result(hypothesis_id: str, raw: dict, output_dir: Path) -> VerificationResult:
    """Parse the agent's result.json into a VerificationResult."""
    from src.schemas import CorrelationResult, FunctionalFormResult, PartialCorrelationResult

    raw_corr = raw.get("raw_correlation")
    partial_corr = raw.get("partial_correlation")
    func_form = raw.get("functional_form")

    # Parse verification_method with graceful fallback for unknown values
    verification_method = None
    raw_method = raw.get("verification_method")
    if raw_method:
        try:
            verification_method = VerificationMethod(raw_method)
        except ValueError:
            logger.warning(
                "Unknown verification_method %r for %s — leaving as None",
                raw_method, hypothesis_id,
            )

    return VerificationResult(
        hypothesis_id=hypothesis_id,
        verdict=Verdict(raw.get("verdict", "inconclusive")),
        verification_method=verification_method,
        raw_correlation=CorrelationResult(**raw_corr) if raw_corr else None,
        partial_correlation=PartialCorrelationResult(**partial_corr) if partial_corr else None,
        functional_form=FunctionalFormResult(**func_form) if func_form else None,
        data_quality_notes=raw.get("data_quality_notes", ""),
        script_path=str(output_dir / "verify.py") if (output_dir / "verify.py").exists() else None,
        summary=raw.get("summary", ""),
    )
