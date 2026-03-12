"""Gradio web UI for the EPI Proxy Discovery Pipeline.

Provides three tabs:
  1. Reports         — browse pre-computed results (research reports + dashboards)
  2. Pipeline Runner — pick an indicator, run the pipeline, see streaming logs + dashboard
  3. Presentation    — embeds the project's presentation.html
"""

import asyncio
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
PRESENTATION2_PATH = PROJECT_ROOT / "presentation2.html"


def _load_presentation() -> str:
    if PRESENTATION_PATH.exists():
        content = PRESENTATION_PATH.read_text(encoding="utf-8")
        return _wrap_in_iframe(content)
    return "<p>presentation.html not found in project root.</p>"


def _load_presentation2() -> str:
    if PRESENTATION2_PATH.exists():
        content = PRESENTATION2_PATH.read_text(encoding="utf-8")
        # Inject the UWD dashboard inline so it works inside srcdoc
        dashboard_path = OUTPUTS_DIR / "UWD" / "dashboard.html"
        if dashboard_path.exists():
            import html as html_mod
            dash_html = dashboard_path.read_text(encoding="utf-8")
            escaped_dash = html_mod.escape(dash_html)
            # Replace the iframe src with srcdoc
            content = content.replace(
                '<iframe id="reportIframe" src="outputs/UWD/dashboard.html" title="UWD Proxy Discovery Dashboard"></iframe>',
                f'<iframe id="reportIframe" srcdoc="{escaped_dash}" title="UWD Proxy Discovery Dashboard" style="width:100%;height:100%;border:none;"></iframe>',
            )
        return _wrap_in_iframe(content)
    return "<p>presentation2.html not found in project root.</p>"


# ── Gradio app ──────────────────────────────────────────────────────────────


_CUSTOM_CSS = """
/* Header banner */
.app-header {
    text-align: center;
    padding: 2rem 1rem 1rem;
    border-bottom: 1px solid #d4d2cb;
    margin-bottom: 1rem;
}
.app-header .tla-badge {
    display: inline-block;
    background: #00356B;
    color: #ffffff;
    font-weight: 700;
    font-size: 0.75rem;
    padding: 0.25rem 0.6rem;
    border-radius: 4px;
    letter-spacing: 0.1em;
    margin-bottom: 0.5rem;
}
.app-header h1 {
    font-family: 'Cormorant Garamond', Georgia, serif;
    font-size: 1.6rem;
    font-weight: 700;
    color: #00356B !important;
    margin: 0.5rem 0 0.25rem;
}
.app-header p {
    color: #8a8a8a;
    font-size: 0.85rem;
    margin: 0;
}

/* Subtle lift on primary buttons */
button.primary:hover {
    box-shadow: 0 2px 8px rgba(0, 53, 107, 0.2) !important;
}

/* Yale blue accent on active tab */
button[role="tab"][aria-selected="true"] {
    color: #00356B !important;
    border-color: #00356B !important;
}

/* Blue focus ring on inputs */
textarea:focus, input:focus {
    border-color: #00356B !important;
    box-shadow: 0 0 0 2px rgba(0, 53, 107, 0.12) !important;
}

/* Thin scrollbar */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #f7f7f5; }
::-webkit-scrollbar-thumb { background: #d4d2cb; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #8a8a8a; }

/* Report hypothesis table */
.report-table td, .report-table th {
    font-size: 12px;
}
"""

_CUSTOM_HEAD = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
    '<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500;600;700&family=Source+Sans+3:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">'
)

# ── Academic theme ─────────────────────────────────────────────────────────────

_THEME = gr.themes.Base(
    primary_hue=gr.themes.Color(
        c50="#e8eef6", c100="#c4d4e8", c200="#9db8d9",
        c300="#7199c9", c400="#4a7dba", c500="#00356B",
        c600="#002d5c", c700="#00244a", c800="#001b38", c900="#001226", c950="#000a16",
    ),
    neutral_hue=gr.themes.Color(
        c50="#fafaf9", c100="#f7f7f5", c200="#eeede9",
        c300="#e8e6e1", c400="#d4d2cb", c500="#b8b5ad",
        c600="#8a8a8a", c700="#5a5a5a", c800="#2c2c2c", c900="#1a1a1a", c950="#0d0d0d",
    ),
    font=[gr.themes.GoogleFont("Source Sans 3"), "system-ui", "sans-serif"],
    font_mono=[gr.themes.GoogleFont("JetBrains Mono"), "monospace"],
).set(
    # Body
    body_background_fill="#ffffff",
    body_background_fill_dark="#ffffff",
    body_text_color="#2c2c2c",
    body_text_color_dark="#2c2c2c",
    body_text_color_subdued="#8a8a8a",
    body_text_color_subdued_dark="#8a8a8a",
    # Blocks
    background_fill_primary="#ffffff",
    background_fill_primary_dark="#ffffff",
    background_fill_secondary="#f7f7f5",
    background_fill_secondary_dark="#f7f7f5",
    block_background_fill="#ffffff",
    block_background_fill_dark="#ffffff",
    block_border_color="#d4d2cb",
    block_border_color_dark="#d4d2cb",
    block_label_background_fill="#f7f7f5",
    block_label_background_fill_dark="#f7f7f5",
    block_label_border_color="#d4d2cb",
    block_label_border_color_dark="#d4d2cb",
    block_label_text_color="#5a5a5a",
    block_label_text_color_dark="#5a5a5a",
    block_title_text_color="#5a5a5a",
    block_title_text_color_dark="#5a5a5a",
    # Borders
    border_color_primary="#d4d2cb",
    border_color_primary_dark="#d4d2cb",
    border_color_accent="#00356B",
    border_color_accent_dark="#00356B",
    # Inputs
    input_background_fill="#f7f7f5",
    input_background_fill_dark="#f7f7f5",
    # Primary button
    button_primary_background_fill="#00356B",
    button_primary_background_fill_dark="#00356B",
    button_primary_background_fill_hover="#2b5f9e",
    button_primary_background_fill_hover_dark="#2b5f9e",
    button_primary_text_color="#ffffff",
    button_primary_text_color_dark="#ffffff",
    button_primary_border_color="#00356B",
    button_primary_border_color_dark="#00356B",
    # Secondary button
    button_secondary_background_fill="transparent",
    button_secondary_background_fill_dark="transparent",
    button_secondary_text_color="#2c2c2c",
    button_secondary_text_color_dark="#2c2c2c",
    button_secondary_border_color="#d4d2cb",
    button_secondary_border_color_dark="#d4d2cb",
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
                for tla in completed:
                    desc = DOMAIN_KNOWLEDGE.get(tla, "").split(")")[0].split("(")[-1] if "(" in DOMAIN_KNOWLEDGE.get(tla, "") else tla
                    indicator_dir = OUTPUTS_DIR / tla

                    # Dashboard iframe
                    dashboard_path = indicator_dir / "dashboard.html"
                    dash_iframe = ""
                    if dashboard_path.exists():
                        dash_iframe = _wrap_in_iframe(
                            dashboard_path.read_text(encoding="utf-8")
                        )

                    # Research report markdown
                    report_path = indicator_dir / "stage1" / "research_report.md"
                    research_md = ""
                    if report_path.exists():
                        research_md = report_path.read_text(encoding="utf-8")

                    with gr.Accordion(f"{tla} — {desc}", open=False):
                        if dash_iframe:
                            with gr.Accordion("Interactive Dashboard", open=True):
                                gr.HTML(dash_iframe)
                        if research_md:
                            with gr.Accordion("Research Report", open=True):
                                gr.Markdown(research_md)

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
        with gr.Tab("Presentation [Technical]"):
            gr.HTML(_load_presentation())

        with gr.Tab("Presentation [EPI]"):
            gr.HTML(_load_presentation2())

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
