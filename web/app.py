"""Gradio web UI for the EPI Proxy Discovery Pipeline.

Provides two tabs:
  1. Pipeline Runner — pick an indicator, run the pipeline, see streaming logs + dashboard
  2. Presentation   — embeds the project's presentation.html
"""

import asyncio
import sys
from pathlib import Path

# Ensure the project root is on sys.path so `src.*` imports work.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import gradio as gr  # noqa: E402

from src.config import OUTPUTS_DIR  # noqa: E402
from src.domain_knowledge import DOMAIN_KNOWLEDGE  # noqa: E402
from src.utils.data_utils import load_variable_metadata  # noqa: E402

# ── Build dropdown choices ──────────────────────────────────────────────────

INDICATOR_CHOICES: list[tuple[str, str]] = []  # (label, tla)
for _tla in sorted(DOMAIN_KNOWLEDGE.keys()):
    try:
        _meta = load_variable_metadata(_tla)
        _desc = _meta.get("Description", _tla)
    except Exception:
        _desc = _tla
    INDICATOR_CHOICES.append((f"{_tla} — {_desc}", _tla))


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
                    yield log_text, dashboard_html, export
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
        return f"Loaded previous results for {tla} from {dashboard_path}", html, export
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
        # Wrap in a sandboxed iframe via srcdoc to isolate styles/scripts
        import html as html_mod
        escaped = html_mod.escape(content)
        return (
            f'<iframe srcdoc="{escaped}" '
            'style="width:100%;height:80vh;border:none;border-radius:8px;" '
            'sandbox="allow-scripts allow-same-origin">'
            "</iframe>"
        )
    return "<p>presentation.html not found in project root.</p>"


# ── Gradio app ──────────────────────────────────────────────────────────────


_CUSTOM_CSS = """
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&display=swap');

:root {
    --bg-primary: #0a0e14;
    --bg-secondary: #131920;
    --accent: #00ff88;
    --accent-dim: #00cc6a;
    --text-primary: #c5cdd8;
    --text-muted: #5c6b7f;
    --border: #1e2a3a;
}

body, .gradio-container {
    background: var(--bg-primary) !important;
    color: var(--text-primary) !important;
    font-family: 'JetBrains Mono', 'SF Mono', 'Consolas', monospace !important;
}

/* Header banner */
.app-header {
    text-align: center;
    padding: 2rem 1rem 1rem;
    border-bottom: 1px solid var(--border);
    margin-bottom: 1rem;
}
.app-header .tla-badge {
    display: inline-block;
    background: var(--accent);
    color: var(--bg-primary);
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
    color: var(--text-muted);
    font-size: 0.85rem;
    margin: 0;
}

/* Panels & containers */
.gr-panel, .gr-box, .gr-form, .gr-group,
div[class*="block"], div[class*="container"] {
    background: var(--bg-primary) !important;
    border-color: var(--border) !important;
}

/* Inputs: textbox, textarea, dropdown */
textarea, input[type="text"], .gr-input, .gr-text-input,
div[data-testid="textbox"] textarea,
.secondary-wrap, .wrap {
    background: var(--bg-secondary) !important;
    color: var(--text-primary) !important;
    border: 1px solid var(--border) !important;
    font-family: 'JetBrains Mono', monospace !important;
    border-radius: 6px !important;
}
textarea:focus, input[type="text"]:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 2px rgba(0, 255, 136, 0.15) !important;
}

/* Dropdown */
.gr-dropdown, div[data-testid="dropdown"] {
    background: var(--bg-secondary) !important;
    border-color: var(--border) !important;
}
.gr-dropdown .options {
    background: var(--bg-secondary) !important;
    border-color: var(--border) !important;
}
.gr-dropdown .option:hover {
    background: var(--border) !important;
}

/* Buttons */
button.primary, button[variant="primary"] {
    background: var(--accent) !important;
    color: var(--bg-primary) !important;
    font-weight: 600 !important;
    border: none !important;
    font-family: 'JetBrains Mono', monospace !important;
    border-radius: 6px !important;
    transition: all 0.2s !important;
}
button.primary:hover, button[variant="primary"]:hover {
    background: var(--accent-dim) !important;
    box-shadow: 0 0 20px rgba(0, 255, 136, 0.25) !important;
}
button.secondary, button[variant="secondary"] {
    background: transparent !important;
    color: var(--text-primary) !important;
    border: 1px solid var(--border) !important;
    font-family: 'JetBrains Mono', monospace !important;
    border-radius: 6px !important;
}
button.secondary:hover, button[variant="secondary"]:hover {
    border-color: var(--accent) !important;
    color: var(--accent) !important;
}

/* Tabs */
button[role="tab"] {
    color: var(--text-muted) !important;
    font-family: 'JetBrains Mono', monospace !important;
    border: none !important;
    background: transparent !important;
}
button[role="tab"][aria-selected="true"] {
    color: var(--accent) !important;
    border-bottom: 2px solid var(--accent) !important;
}

/* Labels */
label, .gr-label, span[data-testid="block-label"] {
    color: var(--text-muted) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.8rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.05em !important;
}

/* Markdown */
.prose, .prose * {
    color: var(--text-primary) !important;
}

/* Scrollbar */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: var(--bg-primary); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--text-muted); }

/* File download */
.file-preview { background: var(--bg-secondary) !important; border-color: var(--border) !important; }
"""

_CUSTOM_HEAD = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">'


def build_app() -> gr.Blocks:
    with gr.Blocks(title="EPI Proxy Discovery") as app:
        gr.HTML(
            '<div class="app-header">'
            '<span class="tla-badge">EPI TOOLS</span>'
            "<h1>Proxy Discovery Pipeline</h1>"
            "<p>Discover and validate data proxies for Yale Environmental Performance Index indicators</p>"
            "</div>"
        )

        with gr.Tab("Pipeline Runner"):
            with gr.Row():
                indicator_dd = gr.Dropdown(
                    choices=INDICATOR_CHOICES,
                    label="EPI Indicator",
                    info="Select an indicator with known domain knowledge",
                )
                run_btn = gr.Button("Run Pipeline", variant="primary")
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

        with gr.Tab("Presentation"):
            gr.HTML(_load_presentation())

    return app


if __name__ == "__main__":
    app = build_app()
    app.launch(
        server_name="0.0.0.0",
        server_port=7860,
        theme=gr.themes.Base(primary_hue="green", neutral_hue="slate"),
        css=_CUSTOM_CSS,
        head=_CUSTOM_HEAD,
    )
