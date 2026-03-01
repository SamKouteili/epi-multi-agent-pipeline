"""HTML dashboard generator for EPI proxy discovery pipeline results."""

from __future__ import annotations

import html
from pathlib import Path
from typing import Optional

from src.config import OUTPUTS_DIR
from src.schemas import (
    PipelineResult,
    ProxyHypothesis,
    ValidationAnnotation,
    VerificationResult,
)


def generate_dashboard(
    result: PipelineResult, output_dir: Path | None = None
) -> Path:
    """Generate a self-contained HTML dashboard for pipeline results.

    Args:
        result: The pipeline result to render.
        output_dir: Directory to write the dashboard into.
            Defaults to ``outputs/{TLA}/``.

    Returns:
        Path to the generated ``dashboard.html`` file.
    """
    if output_dir is None:
        output_dir = OUTPUTS_DIR / result.indicator_tla
    output_dir.mkdir(parents=True, exist_ok=True)

    # Build lookup: hypothesis_id → VerificationResult
    vr_lookup: dict[str, VerificationResult] = {
        vr.hypothesis_id: vr for vr in result.verification_results
    }

    # Determine hypothesis iteration order
    hypotheses: list[ProxyHypothesis] = []
    if result.research_output and result.research_output.hypotheses:
        hypotheses = result.research_output.hypotheses

    # Build table rows
    rows_html = []
    if hypotheses:
        for hyp in hypotheses:
            vr = vr_lookup.get(hyp.id)
            rows_html.append(_build_row(hyp, vr))
    else:
        for vr in result.verification_results:
            rows_html.append(_build_row(None, vr))

    page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{_escape(result.indicator_tla)} — Proxy Discovery Dashboard</title>
<style>
{_build_css()}
</style>
</head>
<body>
{_build_header(result)}
<div class="container">
<table>
<thead>
<tr>
  <th>ID</th>
  <th>Proxy Variable</th>
  <th>Verdict</th>
  <th>r</th>
  <th>p</th>
  <th>n</th>
  <th>Validation</th>
</tr>
<tr>
  <th class="col-source">{_source_tag('s1')}</th>
  <th class="col-source">{_source_tag('s1')}</th>
  <th class="col-source">{_source_tag('s2v')}</th>
  <th class="col-source">{_source_tag('s2v')}</th>
  <th class="col-source">{_source_tag('s2v')}</th>
  <th class="col-source">{_source_tag('s2v')}</th>
  <th class="col-source">{_source_tag('s2val')}</th>
</tr>
</thead>
<tbody>
{"".join(rows_html)}
</tbody>
</table>
</div>
<script>
{_build_js()}
</script>
</body>
</html>"""

    path = output_dir / "dashboard.html"
    path.write_text(page, encoding="utf-8")
    return path


# ── Private helpers ──────────────────────────────────────────────────────────


def _escape(text: object) -> str:
    """HTML-escape any value, converting to string first."""
    return html.escape(str(text)) if text is not None else ""


def _fmt(val: Optional[float], fmt: str = ".3f") -> str:
    """Format a float safely, returning '—' for None."""
    if val is None:
        return "—"
    return f"{val:{fmt}}"


def _verdict_color(verdict: str) -> tuple[str, str, str]:
    """Return (background, text, border) colors for a verdict string."""
    v = verdict.lower().replace(" ", "_")
    colors = {
        "confirmed": ("#002a1a", "#00ff88", "#00ff8844"),
        "partially_confirmed": ("#2a2000", "#ffb800", "#ffb80044"),
        "inconclusive": ("#1a1a1a", "#5c6b7f", "#5c6b7f44"),
        "rejected": ("#2a0010", "#ff4466", "#ff446644"),
    }
    return colors.get(v, ("#1a1a1a", "#5c6b7f", "#5c6b7f44"))


def _source_tag(stage: str) -> str:
    """Return an inline HTML source-origin tag.

    stage: 's1' (research agent), 's2v' (code agent), 's2val' (validator agent).
    """
    labels = {
        "s1": "Research Agent",
        "s2v": "Code Agent",
        "s2val": "Validator Agent",
    }
    return f'<span class="source-tag source-{stage}">{labels.get(stage, stage)}</span>'


def _validation_status(annotation: Optional[ValidationAnnotation]) -> tuple[str, str]:
    """Return (label, color) for the validation column."""
    if annotation is None:
        return ("—", "#5c6b7f")
    n_issues = len(annotation.issues)
    if n_issues == 0:
        return ("clean", "#00ff88")
    return (f"{n_issues} issue{'s' if n_issues != 1 else ''}", "#ffb800")


def _build_css() -> str:
    return """
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
body{
  background:#0a0e14;color:#c5cdd8;
  font-family:'SF Mono','Consolas','Fira Code',monospace;
  font-size:13px;line-height:1.5;padding:24px;
}
.header{
  max-width:1100px;margin:0 auto 24px;
}
.tla-badge{
  display:inline-block;font-size:32px;font-weight:700;
  color:#00ff88;letter-spacing:2px;margin-bottom:8px;
}
.subtitle{color:#5c6b7f;font-size:14px;margin-bottom:12px;}
.chips{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:8px;}
.chip{
  display:inline-flex;align-items:center;gap:4px;
  padding:3px 10px;border-radius:4px;font-size:12px;font-weight:600;
  border:1px solid;
}
.container{max-width:1100px;margin:0 auto;}
table{width:100%;border-collapse:collapse;}
thead th{
  text-align:left;padding:10px 12px;
  color:#5c6b7f;font-size:11px;text-transform:uppercase;letter-spacing:1px;
  border-bottom:1px solid #1e2a3a;
}
.summary-row{cursor:pointer;transition:background .15s;}
.summary-row:hover{background:#131920;}
.summary-row td{
  padding:10px 12px;border-bottom:1px solid #1e2a3a22;
  white-space:nowrap;
}
.summary-row td.proxy-col{white-space:normal;max-width:300px;}
.verdict-badge{
  display:inline-block;padding:2px 8px;border-radius:3px;
  font-size:11px;font-weight:700;letter-spacing:.5px;
  border:1px solid;
}
.detail-row{display:none;}
.detail-row.open{display:table-row;}
.detail-row td{
  padding:0;border-bottom:1px solid #1e2a3a;
}
.detail-panel{
  background:#131920;padding:16px 20px;
  border-left:3px solid #1e2a3a;
}
.detail-panel h4{
  color:#5c6b7f;font-size:11px;text-transform:uppercase;
  letter-spacing:1px;margin:12px 0 6px;
}
.detail-panel h4:first-child{margin-top:0;}
.detail-panel p,.detail-panel li{
  color:#c5cdd8;font-size:12px;line-height:1.6;
}
.detail-panel ul{list-style:none;padding:0;}
.detail-panel ul li::before{content:"› ";color:#5c6b7f;}
.detail-grid{
  display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));
  gap:8px 16px;
}
.detail-stat{display:flex;flex-direction:column;}
.detail-stat .label{color:#5c6b7f;font-size:10px;text-transform:uppercase;letter-spacing:.5px;}
.detail-stat .value{color:#c5cdd8;font-size:13px;}
.flag-chips{display:flex;gap:6px;flex-wrap:wrap;margin-top:4px;}
.flag-chip{
  display:inline-block;padding:1px 6px;border-radius:2px;
  font-size:10px;font-weight:600;letter-spacing:.3px;
}
.flag-pass{background:#002a1a;color:#00ff88;border:1px solid #00ff8833;}
.flag-fail{background:#2a0010;color:#ff4466;border:1px solid #ff446633;}
.not-verified{opacity:0.4;}
.not-verified td{font-style:italic;}
.source-tag{
  display:inline-block;font-size:9px;font-weight:600;
  letter-spacing:.5px;text-transform:uppercase;
  padding:1px 5px;border-radius:2px;margin-left:6px;
  vertical-align:middle;position:relative;top:-1px;
}
.source-s1{background:#1a1a2e;color:#7b8cde;border:1px solid #7b8cde33;}
.source-s2v{background:#1a2a1a;color:#88cc88;border:1px solid #88cc8833;}
.source-s2val{background:#2a1a2a;color:#cc88cc;border:1px solid #cc88cc33;}
thead .col-source{
  font-size:9px;font-weight:400;text-transform:none;
  letter-spacing:0;color:#3d4a5c;padding-top:0;
}
"""


def _build_js() -> str:
    return """
document.addEventListener('DOMContentLoaded',function(){
  document.querySelectorAll('.summary-row').forEach(function(row){
    row.addEventListener('click',function(){
      var id=row.getAttribute('data-id');
      var detail=document.getElementById('detail-'+id);
      if(!detail)return;
      var isOpen=detail.classList.contains('open');
      // close all
      document.querySelectorAll('.detail-row.open').forEach(function(r){r.classList.remove('open');});
      if(!isOpen)detail.classList.add('open');
    });
  });
  document.addEventListener('keydown',function(e){
    if(e.key==='Escape'){
      document.querySelectorAll('.detail-row.open').forEach(function(r){r.classList.remove('open');});
    }
  });
});
"""


def _build_header(result: PipelineResult) -> str:
    """Build the dashboard header with TLA badge and verdict distribution."""
    tla = _escape(result.indicator_tla)

    # Count verdicts
    counts: dict[str, int] = {}
    for vr in result.verification_results:
        v = vr.verdict.value
        counts[v] = counts.get(v, 0) + 1

    # Count unverified hypotheses
    verified_ids = {vr.hypothesis_id for vr in result.verification_results}
    n_unverified = 0
    if result.research_output:
        for hyp in result.research_output.hypotheses:
            if hyp.id not in verified_ids:
                n_unverified += 1

    chips_html = []
    for verdict, count in counts.items():
        bg, fg, bd = _verdict_color(verdict)
        label = verdict.replace("_", " ")
        chips_html.append(
            f'<span class="chip" style="background:{bg};color:{fg};border-color:{bd}">'
            f"{count} {label}</span>"
        )
    if n_unverified:
        chips_html.append(
            '<span class="chip" style="background:#1a1a1a;color:#5c6b7f;border-color:#5c6b7f44">'
            f"{n_unverified} not verified</span>"
        )

    n_hyp = 0
    if result.research_output:
        n_hyp = len(result.research_output.hypotheses)

    subtitle = _escape(result.summary) if result.summary else f"{n_hyp} hypotheses"

    return f"""<div class="header">
<div class="tla-badge">{tla}</div>
<div class="subtitle">{subtitle}</div>
<div class="chips">{"".join(chips_html)}</div>
</div>"""


def _build_detail_panel(
    hyp: Optional[ProxyHypothesis], vr: VerificationResult
) -> str:
    """Build the expandable detail panel for one hypothesis."""
    sections: list[str] = []

    s1 = _source_tag("s1")
    s2v = _source_tag("s2v")
    s2val = _source_tag("s2val")

    # Summary + mechanism
    if hyp:
        sections.append(f"<h4>Summary {s1}</h4><p>{_escape(hyp.proxy_description)}</p>")
        sections.append(f"<h4>Mechanism {s1}</h4><p>{_escape(hyp.mechanism)}</p>")
    if vr.summary:
        sections.append(f"<h4>Verification Summary {s2v}</h4><p>{_escape(vr.summary)}</p>")

    # Partial correlation
    if vr.partial_correlation:
        pc = vr.partial_correlation
        controls = ", ".join(pc.control_variables) if pc.control_variables else "—"
        sections.append(f"""<h4>Partial Correlation {s2v}</h4>
<div class="detail-grid">
  <div class="detail-stat"><span class="label">partial r</span><span class="value">{_fmt(pc.partial_r)}</span></div>
  <div class="detail-stat"><span class="label">partial p</span><span class="value">{_fmt(pc.partial_p, '.4f')}</span></div>
  <div class="detail-stat"><span class="label">controls</span><span class="value">{_escape(controls)}</span></div>
</div>""")

    # Functional form
    if vr.functional_form:
        ff = vr.functional_form
        sections.append(f"""<h4>Functional Form {s2v}</h4>
<div class="detail-grid">
  <div class="detail-stat"><span class="label">best form</span><span class="value">{_escape(ff.best_form.value)}</span></div>
  <div class="detail-stat"><span class="label">linear R²</span><span class="value">{_fmt(ff.linear_r2)}</span></div>
  <div class="detail-stat"><span class="label">log-linear R²</span><span class="value">{_fmt(ff.log_linear_r2)}</span></div>
  <div class="detail-stat"><span class="label">quadratic R²</span><span class="value">{_fmt(ff.quadratic_r2)}</span></div>
  <div class="detail-stat"><span class="label">linear AIC</span><span class="value">{_fmt(ff.linear_aic, '.1f')}</span></div>
  <div class="detail-stat"><span class="label">log-linear AIC</span><span class="value">{_fmt(ff.log_linear_aic, '.1f')}</span></div>
  <div class="detail-stat"><span class="label">quadratic AIC</span><span class="value">{_fmt(ff.quadratic_aic, '.1f')}</span></div>
</div>""")

    # Data quality notes
    if vr.data_quality_notes:
        sections.append(
            f"<h4>Data Quality {s2v}</h4><p>{_escape(vr.data_quality_notes)}</p>"
        )

    # Validation
    if vr.validation:
        va = vr.validation
        flags = [
            ("no synthetic data", va.no_synthetic_data),
            ("year alignment", va.year_alignment_ok),
            ("interpretation", va.hypothesis_interpretation_ok),
            ("authentic source", va.data_source_authentic),
            ("coverage", va.country_coverage_adequate),
            ("no outlier concern", not va.outlier_concerns),
        ]
        flag_chips = []
        for label, ok in flags:
            cls = "flag-pass" if ok else "flag-fail"
            icon = "PASS" if ok else "FAIL"
            flag_chips.append(f'<span class="flag-chip {cls}">{icon} {_escape(label)}</span>')

        sections.append(f'<h4>Validation Flags {s2val}</h4><div class="flag-chips">{"".join(flag_chips)}</div>')

        if va.issues:
            items = "".join(f"<li>{_escape(issue)}</li>" for issue in va.issues)
            sections.append(f"<h4>Issues {s2val}</h4><ul>{items}</ul>")

        if va.mechanistic_explanation:
            sections.append(
                f"<h4>Mechanistic Explanation {s2val}</h4><p>{_escape(va.mechanistic_explanation)}</p>"
            )

        if va.overall_assessment:
            sections.append(
                f"<h4>Overall Assessment {s2val}</h4><p>{_escape(va.overall_assessment)}</p>"
            )
    else:
        sections.append(
            f'<h4>Validation {s2val}</h4>'
            f'<p style="color:#5c6b7f;font-style:italic">Validator agent was not run for this hypothesis.</p>'
        )

    # Caveats + references + data source (from hypothesis)
    if hyp:
        if hyp.caveats:
            items = "".join(f"<li>{_escape(c)}</li>" for c in hyp.caveats)
            sections.append(f"<h4>Caveats {s1}</h4><ul>{items}</ul>")

        if hyp.references:
            items = "".join(f"<li>{_escape(r)}</li>" for r in hyp.references)
            sections.append(f"<h4>References {s1}</h4><ul>{items}</ul>")

        ds = hyp.data_source
        ds_parts = [f"{_escape(ds.name)}"]
        if ds.organization:
            ds_parts.append(f"Organization: {_escape(ds.organization)}")
        if ds.coverage:
            ds_parts.append(f"Coverage: {_escape(ds.coverage)}")
        if ds.accessibility:
            ds_parts.append(f"Access: {_escape(ds.accessibility.value)}")
        sections.append(f"<h4>Data Source {s1}</h4><p>{'<br>'.join(ds_parts)}</p>")

    return f'<div class="detail-panel">{"".join(sections)}</div>'


def _build_row(
    hyp: Optional[ProxyHypothesis], vr: Optional[VerificationResult]
) -> str:
    """Build one summary <tr> and one hidden detail <tr> for a hypothesis."""
    row_id = _escape(hyp.id if hyp else (vr.hypothesis_id if vr else "unknown"))
    proxy_name = _escape(hyp.proxy_variable) if hyp else _escape(row_id)

    if vr is None:
        # No verification result — show greyed out
        return (
            f'<tr class="summary-row not-verified" data-id="{row_id}">'
            f"<td>{row_id}</td>"
            f'<td class="proxy-col">{proxy_name}</td>'
            f'<td><span class="verdict-badge" style="background:#1a1a1a;color:#5c6b7f;border-color:#5c6b7f44">not verified</span></td>'
            f"<td>—</td><td>—</td><td>—</td><td>—</td>"
            f"</tr>\n"
        )

    # Verdict badge
    bg, fg, bd = _verdict_color(vr.verdict.value)
    verdict_label = _escape(vr.verdict.value.replace("_", " "))
    verdict_html = (
        f'<span class="verdict-badge" style="background:{bg};color:{fg};border-color:{bd}">'
        f"{verdict_label}</span>"
    )

    # Stats
    r_val = "—"
    p_val = "—"
    n_val = "—"
    if vr.raw_correlation:
        r_val = _fmt(vr.raw_correlation.pearson_r)
        p_val = _fmt(vr.raw_correlation.pearson_p, ".2e")
        n_val = str(vr.raw_correlation.n_observations) if vr.raw_correlation.n_observations else "—"

    # Validation
    val_label, val_color = _validation_status(vr.validation)

    summary_tr = (
        f'<tr class="summary-row" data-id="{row_id}">'
        f"<td>{row_id}</td>"
        f'<td class="proxy-col">{proxy_name}</td>'
        f"<td>{verdict_html}</td>"
        f"<td>{r_val}</td>"
        f"<td>{p_val}</td>"
        f"<td>{n_val}</td>"
        f'<td style="color:{val_color}">{_escape(val_label)}</td>'
        f"</tr>\n"
    )

    detail_tr = (
        f'<tr class="detail-row" id="detail-{row_id}">'
        f'<td colspan="7">{_build_detail_panel(hyp, vr)}</td>'
        f"</tr>\n"
    )

    return summary_tr + detail_tr
