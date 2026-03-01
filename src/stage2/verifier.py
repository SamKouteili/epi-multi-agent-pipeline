"""Stage 2: Hypothesis verification using Claude Code SDK."""

import json
import logging
import os
from pathlib import Path

from claude_code_sdk import ClaudeCodeOptions, ResultMessage, AssistantMessage, TextBlock, query

from src.config import PROJECT_ROOT, RAW_DIR, OUTPUTS_DIR, CLAUDE_VERIFICATION_MODEL
from src.schemas import ProxyHypothesis, VerificationMethod, VerificationResult, Verdict
from src.stage2.prompts import VERIFIER_SYSTEM_PROMPT, build_verification_prompt
from src.stage2.data_loader import prepare_verification_context

logger = logging.getLogger(__name__)


async def verify_hypothesis(
    hypothesis: ProxyHypothesis,
    tla: str,
    output_dir: Path | None = None,
    prompt_override: str | None = None,
) -> VerificationResult:
    """Verify a single proxy hypothesis using a Claude Code agent.

    The agent downloads proxy data, runs statistical tests, and writes results.

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

    options = ClaudeCodeOptions(
        allowed_tools=["Bash", "Write", "Read", "Glob", "Grep", "WebFetch"],
        permission_mode="bypassPermissions",
        cwd=str(PROJECT_ROOT),
        max_turns=30,
        system_prompt=system_prompt,
        model=CLAUDE_VERIFICATION_MODEL,
    )

    # Collect agent text output
    agent_output_lines = []

    # Temporarily unset CLAUDECODE to allow nested Claude Code sessions
    saved_claudecode = os.environ.pop("CLAUDECODE", None)
    try:
        async for message in query(prompt=verification_prompt, options=options):
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        agent_output_lines.append(block.text)
                        logger.debug("Agent: %s", block.text[:200])
            elif isinstance(message, ResultMessage):
                logger.info(
                    "Agent finished for %s: cost=$%.4f, turns=%s",
                    hypothesis.id,
                    message.total_cost_usd or 0,
                    message.num_turns,
                )
    except Exception as e:
        logger.error("Agent failed for %s: %s", hypothesis.id, e)
        agent_tail = "\n".join(agent_output_lines[-5:]).strip() if agent_output_lines else ""
        # Save whatever output we collected before the crash
        agent_log_path = output_dir / "agent_output.txt"
        agent_log_path.write_text("\n".join(agent_output_lines), encoding="utf-8")
        return VerificationResult(
            hypothesis_id=hypothesis.id,
            verdict=Verdict.inconclusive,
            data_quality_notes=f"Agent execution failed: {e}\n\nAgent output (last lines):\n{agent_tail}",
            summary=f"Verification could not be completed due to agent error: {e}",
        )
    finally:
        if saved_claudecode is not None:
            os.environ["CLAUDECODE"] = saved_claudecode

    # Save agent output
    agent_log_path = output_dir / "agent_output.txt"
    agent_log_path.write_text("\n".join(agent_output_lines), encoding="utf-8")

    # Extract tail of agent output for failure diagnostics
    agent_tail = "\n".join(agent_output_lines[-5:]).strip() if agent_output_lines else ""

    # Fixup: check if result.json was written to PROJECT_ROOT instead of output_dir
    result_path = output_dir / "result.json"
    misplaced_path = PROJECT_ROOT / "result.json"
    if not result_path.exists() and misplaced_path.exists():
        logger.warning(
            "Fixup: result.json found at PROJECT_ROOT instead of %s — moving it",
            output_dir,
        )
        import shutil
        shutil.move(str(misplaced_path), str(result_path))

    # Parse result.json written by the agent
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
                script_path=str(output_dir / "verify.py") if (output_dir / "verify.py").exists() else None,
                summary="Agent completed but result.json could not be parsed.",
            )
    else:
        logger.warning("No result.json found for %s", hypothesis.id)
        return VerificationResult(
            hypothesis_id=hypothesis.id,
            verdict=Verdict.inconclusive,
            data_quality_notes=f"Agent did not produce result.json\n\nAgent output (last lines):\n{agent_tail}",
            script_path=str(output_dir / "verify.py") if (output_dir / "verify.py").exists() else None,
            summary="Verification incomplete — no result.json produced.",
        )


def _fixup_result_json(raw: dict, hypothesis_id: str) -> dict:
    """Apply common fixups to agent-produced result.json before parsing."""
    # Strip "Verdict." prefix from verdict values (e.g. "Verdict.confirmed" → "confirmed")
    verdict = raw.get("verdict", "")
    if isinstance(verdict, str) and verdict.startswith("Verdict."):
        fixed = verdict.split(".", 1)[1]
        logger.warning(
            "Fixup %s: stripped Verdict prefix: %r → %r", hypothesis_id, verdict, fixed
        )
        raw["verdict"] = fixed

    # Normalize uppercase verdict values (e.g. "CONFIRMED" → "confirmed")
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
