"""CLI and pipeline orchestration for the EPI proxy discovery pipeline."""

import argparse
import asyncio
import json
import logging
import sys
import traceback
from collections.abc import AsyncGenerator
from pathlib import Path

from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt

from src.config import OUTPUTS_DIR, API_RETRY_ATTEMPTS, API_RETRY_BACKOFF, MAX_HYPOTHESES
from src.schemas import EvidenceType, PipelineResult, ProxyHypothesis, ResearchOutput, VerificationMethod, VerificationResult, Verdict
from src.utils.data_utils import load_variable_metadata, get_available_indicators

console = Console()
logger = logging.getLogger("epi_proxy")


def setup_logging(tla: str, verbose: bool = False) -> None:
    """Configure logging to both console and file."""
    level = logging.DEBUG if verbose else logging.INFO
    log_dir = OUTPUTS_DIR / tla
    log_dir.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.StreamHandler(sys.stderr),
            logging.FileHandler(log_dir / "pipeline.log", encoding="utf-8"),
        ],
    )


def list_indicators() -> None:
    """Print all available EPI indicators."""
    indicators = get_available_indicators()
    table = Table(title="EPI Indicators")
    table.add_column("TLA", style="cyan")
    table.add_column("Name", style="white")
    table.add_column("Category", style="green")
    table.add_column("Source", style="yellow")
    table.add_column("Units", style="dim")

    for ind in indicators:
        table.add_row(
            str(ind.get("Abbreviation", "")),
            str(ind.get("Description", "")),
            str(ind.get("IssueCategory", "")),
            str(ind.get("Source", "")),
            str(ind.get("Units", "")),
        )

    console.print(table)


async def run_stage1(tla: str, metadata: dict) -> ResearchOutput:
    """Run Stage 1: deep research + hypothesis parsing."""
    from src.stage1.research import run_deep_research
    from src.stage1.parser import parse_research_report

    console.print(f"\n[bold blue]Stage 1: Deep Research for {tla}[/bold blue]")

    # Run research with retries
    markdown, citations = None, []
    for attempt in range(1, API_RETRY_ATTEMPTS + 1):
        try:
            markdown, citations = run_deep_research(tla, metadata)
            break
        except Exception as e:
            logger.warning("Research attempt %d failed: %s", attempt, e)
            if attempt == API_RETRY_ATTEMPTS:
                raise
            await asyncio.sleep(API_RETRY_BACKOFF ** attempt)

    console.print(f"  Research report: {len(markdown)} chars, {len(citations)} citations")

    # Parse with retries
    research_output = None
    for attempt in range(1, API_RETRY_ATTEMPTS + 1):
        try:
            research_output = parse_research_report(tla, markdown, citations, metadata)
            break
        except Exception as e:
            logger.warning("Parsing attempt %d failed: %s", attempt, e)
            if attempt == API_RETRY_ATTEMPTS:
                raise
            await asyncio.sleep(API_RETRY_BACKOFF ** attempt)

    console.print(f"  Parsed {len(research_output.hypotheses)} hypotheses")
    return research_output


def review_hypotheses(hypotheses: list[ProxyHypothesis]) -> list[ProxyHypothesis]:
    """Interactive review: let user approve/reject hypotheses."""
    table = Table(title="Proxy Hypotheses")
    table.add_column("#", style="cyan")
    table.add_column("ID", style="white")
    table.add_column("Proxy Variable", style="green")
    table.add_column("Direction", style="yellow")
    table.add_column("Confidence", style="magenta")
    table.add_column("Evidence", style="blue")
    table.add_column("Data Source", style="dim")

    for i, h in enumerate(hypotheses):
        table.add_row(
            str(i + 1),
            h.id,
            h.proxy_variable,
            h.relationship.direction.value,
            h.confidence.value,
            h.evidence_type.value,
            h.data_source.name[:40],
        )

    console.print(table)
    console.print()

    choice = Prompt.ask(
        "Enter hypothesis numbers to verify (e.g. '1,3,5'), 'all', or 'none'",
        default="all",
    )

    if choice.strip().lower() == "none":
        return []
    if choice.strip().lower() == "all":
        return hypotheses

    indices = []
    for part in choice.split(","):
        part = part.strip()
        if part.isdigit():
            idx = int(part) - 1
            if 0 <= idx < len(hypotheses):
                indices.append(idx)

    return [hypotheses[i] for i in indices]


async def run_stage2(
    tla: str,
    hypotheses: list[ProxyHypothesis],
    max_hypotheses: int = MAX_HYPOTHESES,
) -> list[VerificationResult]:
    """Run Stage 2: verify each hypothesis, routing by evidence_type."""
    from src.stage2.verifier import verify_hypothesis
    from src.stage2.prompts import build_corroboration_prompt, build_exploratory_prompt, build_verification_prompt
    from src.stage2.data_loader import prepare_verification_context

    console.print(f"\n[bold blue]Stage 2: Verification for {tla}[/bold blue]")

    hypotheses = hypotheses[:max_hypotheses]

    # Partition by evidence type
    to_verify = []      # programmatic_verify
    to_corroborate = []  # literature_attested
    to_explore = []      # manual_data_needed

    for hyp in hypotheses:
        if hyp.evidence_type == EvidenceType.manual_data_needed:
            to_explore.append(hyp)
        elif hyp.evidence_type == EvidenceType.literature_attested:
            to_corroborate.append(hyp)
        else:
            to_verify.append(hyp)

    if to_verify:
        console.print(f"  Verifying {len(to_verify)} programmatic hypothesis(es)")
    if to_explore:
        console.print(f"  [magenta]Exploring {len(to_explore)} hypothesis(es) requiring data discovery[/magenta]")
    if to_corroborate:
        console.print(f"  [blue]Corroborating {len(to_corroborate)} literature-attested hypothesis(es)[/blue]")

    results = []
    used_sources: list[str] = []  # Track proxy data sources to prevent deduplication

    # Build ordered work list: programmatic → exploratory → corroboration
    work_items: list[tuple[ProxyHypothesis, str]] = []
    for hyp in to_verify:
        work_items.append((hyp, "verification"))
    for hyp in to_explore:
        work_items.append((hyp, "exploratory"))
    for hyp in to_corroborate:
        work_items.append((hyp, "corroboration"))

    # Execute sequentially
    data_summary = prepare_verification_context(tla)
    total = len(work_items)

    _work_type_labels = {
        "verification": "Verifying",
        "exploratory": "Exploring",
        "corroboration": "Corroborating",
    }
    _work_type_fallback_method = {
        "verification": VerificationMethod.statistical_test,
        "exploratory": VerificationMethod.pending_data,
        "corroboration": VerificationMethod.literature_accepted,
    }

    for i, (hyp, work_type) in enumerate(work_items, 1):
        label = _work_type_labels.get(work_type, "Verifying")
        console.print(f"\n  [{i}/{total}] {label} {hyp.id}: {hyp.proxy_variable}")

        # Build prompt at execution time so it includes up-to-date used_sources
        output_dir = OUTPUTS_DIR / tla / "stage2" / hyp.id
        output_dir.mkdir(parents=True, exist_ok=True)
        if work_type == "corroboration":
            prompt_override = build_corroboration_prompt(
                hyp, tla, data_summary, output_dir, used_sources=used_sources,
            )
        elif work_type == "exploratory":
            prompt_override = build_exploratory_prompt(
                hyp, tla, data_summary, output_dir, used_sources=used_sources,
            )
        else:
            prompt_override = build_verification_prompt(
                hyp, tla, data_summary, output_dir, used_sources=used_sources,
            )

        try:
            result = await verify_hypothesis(hyp, tla, prompt_override=prompt_override)

            # Infer verification_method from work_type if agent didn't set it
            if result.verification_method is None:
                result.verification_method = _work_type_fallback_method.get(work_type)

            results.append(result)

            # Track data source for deduplication
            source_label = f"{hyp.data_source.name} (used by {hyp.id})"
            used_sources.append(source_label)
            verdict_color = {
                "confirmed": "green",
                "partially_confirmed": "yellow",
                "inconclusive": "dim",
                "rejected": "red",
            }.get(result.verdict.value, "white")
            method_str = result.verification_method.value if result.verification_method else "unknown"
            console.print(f"    Verdict: [{verdict_color}]{result.verdict.value}[/{verdict_color}]  Method: {method_str}")
            if result.summary:
                console.print(f"    Summary: {result.summary[:120]}")

            # Run validation agent (non-fatal)
            try:
                from src.stage2.validator import validate_result

                annotation = await validate_result(hyp, result, output_dir)
                if annotation:
                    result.validation = annotation
                    n_issues = len(annotation.issues)
                    if n_issues == 0:
                        console.print("    Validation: [green]clean[/green]")
                    else:
                        console.print(f"    Validation: [yellow]{n_issues} issue(s)[/yellow]")
            except Exception as val_err:
                logger.debug("Validation failed for %s: %s", hyp.id, val_err)

        except Exception as e:
            logger.error("Verification failed for %s: %s", hyp.id, e)
            results.append(VerificationResult(
                hypothesis_id=hyp.id,
                verdict=Verdict.inconclusive,
                data_quality_notes=f"Verification error: {e}",
                summary=f"Error during verification: {e}",
            ))

    return results


def print_summary(result: PipelineResult) -> None:
    """Print a final summary table of the pipeline results."""
    console.print(f"\n[bold]Pipeline Results for {result.indicator_tla}[/bold]")

    if result.research_output:
        console.print(f"  Hypotheses generated: {len(result.research_output.hypotheses)}")

    if result.verification_results:
        # Build lookup from hypothesis_id → evidence_type
        hyp_evidence = {}
        if result.research_output:
            for h in result.research_output.hypotheses:
                hyp_evidence[h.id] = h.evidence_type.value

        table = Table(title="Verification Results")
        table.add_column("Hypothesis", style="cyan")
        table.add_column("Type", style="blue")
        table.add_column("Method", style="magenta")
        table.add_column("Verdict", style="white")
        table.add_column("Pearson r", style="green")
        table.add_column("p-value", style="yellow")
        table.add_column("n", style="dim")
        table.add_column("Validation", style="white")
        table.add_column("Summary")

        for vr in result.verification_results:
            r_val = ""
            p_val = ""
            n_val = ""
            if vr.raw_correlation:
                r_val = f"{vr.raw_correlation.pearson_r:.3f}" if vr.raw_correlation.pearson_r is not None else ""
                p_val = f"{vr.raw_correlation.pearson_p:.4f}" if vr.raw_correlation.pearson_p is not None else ""
                n_val = str(vr.raw_correlation.n_observations or "")

            verdict_color = {
                "confirmed": "green",
                "partially_confirmed": "yellow",
                "inconclusive": "dim",
                "rejected": "red",
            }.get(vr.verdict.value, "white")

            method_val = vr.verification_method.value if vr.verification_method else ""

            # Validation status
            if vr.validation:
                n_issues = len(vr.validation.issues)
                val_str = "[green]clean[/green]" if n_issues == 0 else f"[yellow]{n_issues} issue(s)[/yellow]"
            else:
                val_str = "[dim]—[/dim]"

            table.add_row(
                vr.hypothesis_id,
                hyp_evidence.get(vr.hypothesis_id, ""),
                method_val,
                f"[{verdict_color}]{vr.verdict.value}[/{verdict_color}]",
                r_val,
                p_val,
                n_val,
                val_str,
                (vr.summary[:60] + "...") if len(vr.summary) > 60 else vr.summary,
            )

        console.print(table)

    console.print(f"\n  Full results: {OUTPUTS_DIR / result.indicator_tla / 'pipeline_result.json'}")
    console.print(f"  Dashboard: {OUTPUTS_DIR / result.indicator_tla / 'dashboard.html'}")


async def run_pipeline(args: argparse.Namespace) -> None:
    """Main pipeline orchestration."""
    tla = args.indicator.upper()
    setup_logging(tla, args.verbose)

    # Load metadata
    try:
        metadata = load_variable_metadata(tla)
    except ValueError as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)

    console.print(f"[bold]EPI Proxy Discovery Pipeline — {tla}[/bold]")
    console.print(f"  {metadata.get('Description', tla)} ({metadata.get('Units', '')})")

    research_output = None
    hypotheses = []

    # Stage 1
    if args.stage in ("1", "both"):
        research_output = await run_stage1(tla, metadata)
        hypotheses = research_output.hypotheses

    # Load pre-existing hypotheses if specified
    if args.hypotheses_file:
        hyp_path = Path(args.hypotheses_file)
        if not hyp_path.exists():
            console.print(f"[red]Hypotheses file not found: {hyp_path}[/red]")
            sys.exit(1)
        raw = json.loads(hyp_path.read_text(encoding="utf-8"))
        research_output = ResearchOutput(
            indicator_tla=tla,
            hypotheses=[ProxyHypothesis.model_validate(h) for h in raw.get("hypotheses", [])],
            causal_map_summary=raw.get("causal_map_summary", ""),
            raw_report_path=str(hyp_path),
        )
        hypotheses = research_output.hypotheses
        console.print(f"  Loaded {len(hypotheses)} hypotheses from {hyp_path}")

    # Review
    if args.review and hypotheses:
        hypotheses = review_hypotheses(hypotheses)
        if not hypotheses:
            console.print("[yellow]No hypotheses selected. Exiting.[/yellow]")
            return

    # Stage 2
    verification_results = []
    if args.stage in ("2", "both") and hypotheses:
        verification_results = await run_stage2(tla, hypotheses, args.max_hypotheses)

    # Aggregate results
    pipeline_result = PipelineResult(
        indicator_tla=tla,
        research_output=research_output,
        verification_results=verification_results,
        summary=f"Completed pipeline for {tla}: "
        f"{len(hypotheses)} hypotheses, {len(verification_results)} verified",
    )

    # Save
    output_path = OUTPUTS_DIR / tla / "pipeline_result.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(pipeline_result.model_dump_json(indent=2), encoding="utf-8")

    from src.report import generate_dashboard
    dashboard_path = generate_dashboard(pipeline_result)
    console.print(f"  Dashboard: {dashboard_path}")

    print_summary(pipeline_result)


class _ListHandler(logging.Handler):
    """Logging handler that appends formatted records to a list."""

    def __init__(self, sink: list[str]) -> None:
        super().__init__()
        self.sink = sink

    def emit(self, record: logging.LogRecord) -> None:
        try:
            self.sink.append(self.format(record))
        except Exception:
            pass


async def run_pipeline_headless(tla: str) -> AsyncGenerator[tuple[str, str | None], None]:
    """Run the full pipeline for *tla*, yielding ``(log_text, dashboard_html)`` tuples.

    Designed for the Gradio web UI — no Rich markup, no interactive prompts,
    no ``sys.exit``.  Each yield contains the **accumulated** log so far and
    either ``None`` (still running) or the dashboard HTML string (done).
    """
    tla = tla.upper()
    lines: list[str] = []

    # Set up logging into our list (file handler still writes to disk)
    log_dir = OUTPUTS_DIR / tla
    log_dir.mkdir(parents=True, exist_ok=True)

    handler = _ListHandler(lines)
    handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
    root_logger = logging.getLogger()
    root_logger.addHandler(handler)
    root_logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler(log_dir / "pipeline.log", encoding="utf-8")
    file_handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
    root_logger.addHandler(file_handler)

    def _log(msg: str) -> str:
        lines.append(msg)
        logger.info(msg)
        return "\n".join(lines)

    try:
        # Load metadata
        try:
            metadata = load_variable_metadata(tla)
        except ValueError as e:
            yield (_log(f"ERROR: {e}"), None)
            return

        desc = metadata.get("Description", tla)
        units = metadata.get("Units", "")
        yield (_log(f"=== EPI Proxy Discovery Pipeline — {tla} ==="), None)
        yield (_log(f"  {desc} ({units})"), None)

        # Stage 1
        yield (_log(f"\n--- Stage 1: Deep Research for {tla} ---"), None)
        research_output = await run_stage1(tla, metadata)
        hypotheses = research_output.hypotheses
        yield (_log(f"  Parsed {len(hypotheses)} hypotheses"), None)

        # Stage 2
        if hypotheses:
            yield (_log(f"\n--- Stage 2: Verification for {tla} ---"), None)
            verification_results = await run_stage2(tla, hypotheses)
            yield (_log(f"  Verified {len(verification_results)} hypotheses"), None)
        else:
            verification_results = []
            yield (_log("  No hypotheses to verify"), None)

        # Aggregate
        pipeline_result = PipelineResult(
            indicator_tla=tla,
            research_output=research_output,
            verification_results=verification_results,
            summary=f"Completed pipeline for {tla}: "
            f"{len(hypotheses)} hypotheses, {len(verification_results)} verified",
        )

        # Save
        output_path = OUTPUTS_DIR / tla / "pipeline_result.json"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(pipeline_result.model_dump_json(indent=2), encoding="utf-8")

        # Dashboard
        from src.report import generate_dashboard

        dashboard_path = generate_dashboard(pipeline_result)
        yield (_log(f"\n  Dashboard saved: {dashboard_path}"), None)

        dashboard_html = dashboard_path.read_text(encoding="utf-8")
        yield ("\n".join(lines), dashboard_html)

    except Exception:
        yield (_log(f"\nERROR:\n{traceback.format_exc()}"), None)
    finally:
        root_logger.removeHandler(handler)
        root_logger.removeHandler(file_handler)
        file_handler.close()


def main() -> None:
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        prog="epi-proxy-discovery",
        description="Discover and validate data proxies for EPI indicators",
    )
    parser.add_argument(
        "--indicator", "-i",
        type=str,
        help="EPI indicator TLA (e.g., UWD, WRR)",
    )
    parser.add_argument(
        "--stage", "-s",
        choices=["1", "2", "both"],
        default="both",
        help="Which pipeline stage(s) to run (default: both)",
    )
    parser.add_argument(
        "--review",
        action="store_true",
        help="Interactively review hypotheses before verification",
    )
    parser.add_argument(
        "--hypotheses-file",
        type=str,
        help="Path to pre-existing hypotheses JSON (skips Stage 1)",
    )
    parser.add_argument(
        "--max-hypotheses",
        type=int,
        default=MAX_HYPOTHESES,
        help=f"Maximum hypotheses to verify (default: {MAX_HYPOTHESES})",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose logging",
    )
    parser.add_argument(
        "--list-indicators",
        action="store_true",
        help="List all available EPI indicators and exit",
    )

    args = parser.parse_args()

    if args.list_indicators:
        list_indicators()
        return

    if not args.indicator:
        parser.error("--indicator is required (or use --list-indicators)")

    asyncio.run(run_pipeline(args))
