"""Gradio web UI for the EPI Proxy Discovery Pipeline.

Provides three tabs:
  1. Reports         — browse pre-computed results (research reports + dashboards)
  2. Pipeline Runner — pick an indicator, run the pipeline, see streaming logs + dashboard
  3. Presentation    — embeds the project's presentation.html
"""

import asyncio
import json
import sys
from pathlib import Path

# Ensure the project root is on sys.path so `src.*` imports work.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import gradio as gr  # noqa: E402

from src.config import OUTPUTS_DIR, MASTER_VARIABLE_LIST  # noqa: E402
from src.domain_knowledge import DOMAIN_KNOWLEDGE  # noqa: E402

import pandas as _pd  # noqa: E402

# ── Build dropdown choices ──────────────────────────────────────────────────

try:
    _variable_meta = {
        row["Abbreviation"]: row
        for _, row in _pd.read_csv(MASTER_VARIABLE_LIST).iterrows()
    }
except FileNotFoundError:
    _variable_meta = {}

INDICATOR_CHOICES: list[tuple[str, str]] = []  # (label, tla)
for _tla in sorted(DOMAIN_KNOWLEDGE.keys()):
    _desc = _variable_meta.get(_tla, {}).get("Description", _tla)
    INDICATOR_CHOICES.append((f"{_tla} — {_desc}", _tla))


# ── Helpers ────────────────────────────────────────────────────────────────


def _wrap_in_iframe(html_content: str, height: str = "80vh") -> str:
    """Wrap HTML in a sandboxed iframe so embedded scripts execute."""
    import html as html_mod
    escaped = html_mod.escape(html_content)
    return (
        f'<iframe srcdoc="{escaped}" '
        f'style="width:100%;height:{height};border:none;border-radius:8px;" '
        'sandbox="allow-scripts allow-same-origin">'
        '</iframe>'
    )


def _get_completed_indicators() -> list[str]:
    """Return sorted list of TLAs that have completed pipeline runs."""
    if not OUTPUTS_DIR.exists():
        return []
    return sorted(
        d.name for d in OUTPUTS_DIR.iterdir()
        if d.is_dir() and (d / "pipeline_result.json").exists()
    )


def _verdict_badge(verdict: str) -> str:
    """Return an HTML badge for a hypothesis verdict."""
    colors = {
        "confirmed": ("#00ff88", "#0a0e14"),
        "partially_confirmed": ("#ffb800", "#0a0e14"),
        "inconclusive": ("#5c6b7f", "#c5cdd8"),
        "rejected": ("#ff4444", "#ffffff"),
    }
    bg, fg = colors.get(verdict, ("#5c6b7f", "#c5cdd8"))
    label = verdict.replace("_", " ").title()
    return (
        f'<span style="background:{bg};color:{fg};padding:2px 8px;'
        f'border-radius:4px;font-size:12px;font-weight:600;">{label}</span>'
    )


def _load_hypothesis_results(tla: str) -> list[dict]:
    """Load all hypothesis result.json files for a given indicator."""
    stage2_dir = OUTPUTS_DIR / tla / "stage2"
    if not stage2_dir.exists():
        return []
    results = []
    for hyp_dir in sorted(stage2_dir.iterdir()):
        result_file = hyp_dir / "result.json"
        if result_file.exists():
            try:
                data = json.loads(result_file.read_text(encoding="utf-8"))
                data["_dir"] = hyp_dir.name
                results.append(data)
            except (json.JSONDecodeError, OSError):
                pass
    return results


def _load_hypotheses(tla: str) -> list[dict]:
    """Load hypotheses.json from stage1."""
    hyp_file = OUTPUTS_DIR / tla / "stage1" / "hypotheses.json"
    if not hyp_file.exists():
        return []
    try:
        data = json.loads(hyp_file.read_text(encoding="utf-8"))
        if isinstance(data, dict) and "hypotheses" in data:
            return data["hypotheses"]
        if isinstance(data, list):
            return data
    except (json.JSONDecodeError, OSError):
        pass
    return []


# ── Reports tab logic ─────────────────────────────────────────────────────


def load_report(tla: str) -> tuple[str, str, str]:
    """Load the full report view for a given indicator.

    Returns (summary_html, research_md, dashboard_iframe).
    """
    if not tla:
        return "", "*Select an indicator above.*", ""

    indicator_dir = OUTPUTS_DIR / tla
    if not indicator_dir.exists():
        return "", f"*No results found for {tla}.*", ""

    # ── Summary card with hypothesis results ──
    hypotheses = _load_hypotheses(tla)
    results = _load_hypothesis_results(tla)
    results_by_id = {r.get("hypothesis_id", ""): r for r in results}

    # Count verdicts
    verdict_counts: dict[str, int] = {}
    for r in results:
        v = r.get("verdict", "unknown")
        verdict_counts[v] = verdict_counts.get(v, 0) + 1

    summary_parts = [f'<div style="margin-bottom:16px;">']
    summary_parts.append(
        f'<span style="font-size:24px;font-weight:700;color:#00ff88;">{tla}</span>'
        f'<span style="color:#5c6b7f;margin-left:12px;">'
        f'{_variable_meta.get(tla, {}).get("Description", "")}</span>'
    )
    summary_parts.append('<div style="margin-top:8px;display:flex;gap:12px;">')
    for v, count in sorted(verdict_counts.items()):
        summary_parts.append(f'{_verdict_badge(v)} <span style="color:#5c6b7f;">x{count}</span>')
    summary_parts.append('</div></div>')

    # Hypothesis table
    if hypotheses or results:
        summary_parts.append(
            '<table style="width:100%;border-collapse:collapse;margin-top:12px;">'
            '<tr style="border-bottom:1px solid #1e2a3a;color:#5c6b7f;font-size:12px;">'
            '<th style="text-align:left;padding:6px;">ID</th>'
            '<th style="text-align:left;padding:6px;">Proxy Variable</th>'
            '<th style="text-align:left;padding:6px;">Verdict</th>'
            '<th style="text-align:left;padding:6px;">Correlation</th>'
            '<th style="text-align:left;padding:6px;">N</th>'
            '</tr>'
        )
        for h in hypotheses:
            hid = h.get("id", "")
            proxy = h.get("proxy_variable", h.get("proxy_description", "—"))
            r = results_by_id.get(hid, {})
            verdict = r.get("verdict", "pending")
            biv = r.get("bivariate_correlation", {})
            if isinstance(biv, dict) and biv.get("r") is not None:
                corr_str = f'r={biv["r"]:.3f} (p={biv.get("p_value", "?"):.2e})'
            else:
                corr_str = "—"
            n = r.get("n_observations", "—")
            summary_parts.append(
                f'<tr style="border-bottom:1px solid #131920;">'
                f'<td style="padding:6px;font-weight:600;color:#c5cdd8;">{hid}</td>'
                f'<td style="padding:6px;color:#a3adb8;max-width:300px;'
                f'overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">{proxy}</td>'
                f'<td style="padding:6px;">{_verdict_badge(verdict)}</td>'
                f'<td style="padding:6px;color:#c5cdd8;">{corr_str}</td>'
                f'<td style="padding:6px;color:#5c6b7f;">{n}</td>'
                f'</tr>'
            )
        summary_parts.append('</table>')

    summary_html = "\n".join(summary_parts)

    # ── Research report markdown ──
    report_path = indicator_dir / "stage1" / "research_report.md"
    if report_path.exists():
        research_md = report_path.read_text(encoding="utf-8")
    else:
        research_md = "*No research report found.*"

    # ── Dashboard iframe ──
    dashboard_path = indicator_dir / "dashboard.html"
    if dashboard_path.exists():
        dash_html = dashboard_path.read_text(encoding="utf-8")
        dashboard_iframe = _wrap_in_iframe(dash_html)
    else:
        dashboard_iframe = "<p style='color:#5c6b7f;'>No dashboard generated yet.</p>"

    return summary_html, research_md, dashboard_iframe


# ── Pipeline runner (async generator → Gradio streaming) ───────────────────


async def _run_pipeline_async(tla: str):
    """Async generator that drives the headless pipeline."""
    from src.orchestrator import run_pipeline_headless

    async for log_text, dashboard_html in run_pipeline_headless(tla):
        yield log_text, dashboard_html or ""


def run_pipeline_web(tla: str):
    """Synchronous generator wrapper for Gradio — yields (log, dashboard_html, export_file)."""
    if not tla:
        yield "Please select an indicator first.", "", gr.skip()
        return

    yield (
        "Pipeline started — this typically takes ~20 minutes.\n"
        "Stage 1 (research) takes ~5 min, Stage 2 (verification) takes ~15 min.\n"
    ), "", gr.skip()

    loop = asyncio.new_event_loop()
    try:
        agen = _run_pipeline_async(tla)
        while True:
            try:
                log_text, dashboard_html = loop.run_until_complete(agen.__anext__())
                if dashboard_html:
                    # Final yield — pipeline done, provide export file
                    result_path = OUTPUTS_DIR / tla / "pipeline_result.json"
                    export = str(result_path) if result_path.exists() else None
                    yield log_text, _wrap_in_iframe(dashboard_html), export
                else:
                    yield log_text, dashboard_html, gr.skip()
            except StopAsyncIteration:
                break
    finally:
        loop.close()


def load_previous_results(tla: str) -> tuple[str, str, str | None]:
    """If a dashboard already exists for the chosen TLA, return it."""
    if not tla:
        return "", "", None
    dashboard_path = OUTPUTS_DIR / tla / "dashboard.html"
    result_path = OUTPUTS_DIR / tla / "pipeline_result.json"
    if dashboard_path.exists():
        html = dashboard_path.read_text(encoding="utf-8")
        export = str(result_path) if result_path.exists() else None
        return f"Loaded previous results for {tla} from {dashboard_path}", _wrap_in_iframe(html), export
    return f"No previous results found for {tla}.", "", None


def export_results(tla: str) -> str | None:
    """Return the path to pipeline_result.json for download."""
    if not tla:
        return None
    result_path = OUTPUTS_DIR / tla / "pipeline_result.json"
    if result_path.exists():
        return str(result_path)
    return None


# ── Presentation tab ───────────────────────────────────────────────────────

PRESENTATION_PATH = PROJECT_ROOT / "presentation.html"


def _load_presentation() -> str:
    if PRESENTATION_PATH.exists():
        content = PRESENTATION_PATH.read_text(encoding="utf-8")
        return _wrap_in_iframe(content)
    return "<p>presentation.html not found in project root.</p>"


# ── Gradio app ──────────────────────────────────────────────────────────────


_CUSTOM_CSS = """
/* Header banner */
.app-header {
    text-align: center;
    padding: 2rem 1rem 1rem;
    border-bottom: 1px solid #1e2a3a;
    margin-bottom: 1rem;
}
.app-header .tla-badge {
    display: inline-block;
    background: #00ff88;
    color: #0a0e14;
    font-weight: 700;
    font-size: 0.75rem;
    padding: 0.25rem 0.6rem;
    border-radius: 4px;
    letter-spacing: 0.1em;
    margin-bottom: 0.5rem;
}
.app-header h1 {
    font-size: 1.6rem;
    font-weight: 700;
    color: #fff !important;
    margin: 0.5rem 0 0.25rem;
}
.app-header p {
    color: #5c6b7f;
    font-size: 0.85rem;
    margin: 0;
}

/* Neon glow on primary buttons */
button.primary:hover {
    box-shadow: 0 0 20px rgba(0, 255, 136, 0.3) !important;
}

/* Green accent on active tab */
button[role="tab"][aria-selected="true"] {
    color: #00ff88 !important;
    border-color: #00ff88 !important;
}

/* Green focus ring on inputs */
textarea:focus, input:focus {
    border-color: #00ff88 !important;
    box-shadow: 0 0 0 2px rgba(0, 255, 136, 0.15) !important;
}

/* Thin scrollbar */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #0a0e14; }
::-webkit-scrollbar-thumb { background: #1e2a3a; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #5c6b7f; }

/* Report hypothesis table */
.report-table td, .report-table th {
    font-size: 12px;
}
"""

_CUSTOM_HEAD = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
    '<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">'
)

# ── Build dark terminal theme via Gradio's theme API ─────────────────────────

_THEME = gr.themes.Base(
    primary_hue=gr.themes.Color(
        c50="#e6fff3", c100="#b3ffdb", c200="#80ffc4",
        c300="#4dffac", c400="#1aff95", c500="#00ff88",
        c600="#00cc6a", c700="#00994f", c800="#006635", c900="#00331a", c950="#001a0d",
    ),
    neutral_hue=gr.themes.Color(
        c50="#c5cdd8", c100="#a3adb8", c200="#8192a3",
        c300="#5c6b7f", c400="#3d4f63", c500="#2a3a4e",
        c600="#1e2a3a", c700="#131920", c800="#0d1117", c900="#0a0e14", c950="#070a0f",
    ),
    font=gr.themes.GoogleFont("JetBrains Mono"),
    font_mono=gr.themes.GoogleFont("JetBrains Mono"),
).set(
    # Body
    body_background_fill="#0a0e14",
    body_background_fill_dark="#0a0e14",
    body_text_color="#c5cdd8",
    body_text_color_dark="#c5cdd8",
    body_text_color_subdued="#5c6b7f",
    body_text_color_subdued_dark="#5c6b7f",
    # Blocks
    background_fill_primary="#0a0e14",
    background_fill_primary_dark="#0a0e14",
    background_fill_secondary="#131920",
    background_fill_secondary_dark="#131920",
    block_background_fill="#0d1117",
    block_background_fill_dark="#0d1117",
    block_border_color="#1e2a3a",
    block_border_color_dark="#1e2a3a",
    block_label_background_fill="#0a0e14",
    block_label_background_fill_dark="#0a0e14",
    block_label_border_color="#1e2a3a",
    block_label_border_color_dark="#1e2a3a",
    block_label_text_color="#5c6b7f",
    block_label_text_color_dark="#5c6b7f",
    block_title_text_color="#5c6b7f",
    block_title_text_color_dark="#5c6b7f",
    # Borders
    border_color_primary="#1e2a3a",
    border_color_primary_dark="#1e2a3a",
    border_color_accent="#00ff88",
    border_color_accent_dark="#00ff88",
    # Inputs
    input_background_fill="#131920",
    input_background_fill_dark="#131920",
    # Primary button
    button_primary_background_fill="#00ff88",
    button_primary_background_fill_dark="#00ff88",
    button_primary_background_fill_hover="#00cc6a",
    button_primary_background_fill_hover_dark="#00cc6a",
    button_primary_text_color="#0a0e14",
    button_primary_text_color_dark="#0a0e14",
    button_primary_border_color="#00ff88",
    button_primary_border_color_dark="#00ff88",
    # Secondary button
    button_secondary_background_fill="transparent",
    button_secondary_background_fill_dark="transparent",
    button_secondary_text_color="#c5cdd8",
    button_secondary_text_color_dark="#c5cdd8",
    button_secondary_border_color="#1e2a3a",
    button_secondary_border_color_dark="#1e2a3a",
)


def build_app() -> gr.Blocks:
    with gr.Blocks(title="EPI Proxy Discovery") as app:
        gr.HTML(
            '<div class="app-header">'
            '<span class="tla-badge">EPI TOOLS</span>'
            "<h1>Proxy Discovery Pipeline</h1>"
            "<p>Discover and validate data proxies for Yale Environmental Performance Index indicators</p>"
            "</div>"
        )

        # ── Tab 1: Reports ────────────────────────────────────────────────
        with gr.Tab("Reports"):
            completed = _get_completed_indicators()
            if not completed:
                gr.Markdown("_No reports found yet. Run the pipeline to generate results._")
            else:
                report_choices = []
                for tla in completed:
                    desc = _variable_meta.get(tla, {}).get("Description", tla)
                    report_choices.append((f"{tla} — {desc}", tla))

                report_dd = gr.Dropdown(
                    choices=report_choices,
                    label="Select Indicator Report",
                    info=f"{len(completed)} indicator(s) with results",
                    value=completed[0] if completed else None,
                )

                report_summary = gr.HTML(label="Summary")

                with gr.Accordion("Research Report", open=False):
                    report_markdown = gr.Markdown()

                with gr.Accordion("Interactive Dashboard", open=True):
                    report_dashboard = gr.HTML()

                # Load on selection change
                report_dd.change(
                    fn=load_report,
                    inputs=[report_dd],
                    outputs=[report_summary, report_markdown, report_dashboard],
                )

                # Load initial report
                if completed:
                    app.load(
                        fn=load_report,
                        inputs=[report_dd],
                        outputs=[report_summary, report_markdown, report_dashboard],
                    )

        # ── Tab 2: Pipeline Runner ────────────────────────────────────────
        with gr.Tab("Pipeline Runner"):
            with gr.Row():
                indicator_dd = gr.Dropdown(
                    choices=INDICATOR_CHOICES,
                    label="EPI Indicator",
                    info=f"All {len(INDICATOR_CHOICES)} EPI indicators available",
                )
                run_btn = gr.Button("Run Pipeline (~20 min)", variant="primary")
                prev_btn = gr.Button("View Previous Results", variant="secondary")

            log_box = gr.Textbox(
                label="Pipeline Log",
                lines=25,
                max_lines=60,
                interactive=False,
            )
            dashboard_html = gr.HTML(label="Dashboard")
            export_file = gr.File(
                label="Export Results",
                visible=True,
                interactive=False,
            )

            run_btn.click(
                fn=run_pipeline_web,
                inputs=[indicator_dd],
                outputs=[log_box, dashboard_html, export_file],
            )
            prev_btn.click(
                fn=load_previous_results,
                inputs=[indicator_dd],
                outputs=[log_box, dashboard_html, export_file],
            )

        # ── Tab 3: Presentation ───────────────────────────────────────────
        with gr.Tab("Presentation"):
            gr.HTML(_load_presentation())

    return app


if __name__ == "__main__":
    app = build_app()
    app.launch(
        server_name="0.0.0.0",
        server_port=7860,
        theme=_THEME,
        css=_CUSTOM_CSS,
        head=_CUSTOM_HEAD,
    )
