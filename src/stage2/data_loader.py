"""Prepare EPI data context for the verification agent."""

import logging

from src.config import RAW_DIR, CONTROL_VARIABLE_TLAS
from src.utils.data_utils import load_raw_indicator, load_variable_metadata

logger = logging.getLogger(__name__)


def prepare_verification_context(tla: str) -> str:
    """Load the target indicator and summarize coverage for the verification agent prompt.

    Returns a formatted string with data summary and file paths.
    """
    df = load_raw_indicator(tla)
    meta = load_variable_metadata(tla)

    n_countries = df["iso"].nunique()
    year_min = df["year"].min()
    year_max = df["year"].max()
    n_obs = len(df)
    mean_val = df["value"].mean()
    std_val = df["value"].std()
    median_val = df["value"].median()

    summary_lines = [
        f"**Target Indicator**: {tla} — {meta.get('Description', tla)}",
        f"**Units**: {meta.get('Units', 'unknown')}",
        f"**Polarity**: {meta.get('RawPolarity', 'unknown')}",
        f"**Source**: {meta.get('Source', 'unknown')}",
        f"**Data File**: `{RAW_DIR / f'{tla}_raw.csv'}`",
        f"**Coverage**: {n_countries} countries, {year_min}-{year_max} ({n_obs} observations)",
        f"**Summary Stats**: mean={mean_val:.2f}, std={std_val:.2f}, median={median_val:.2f}",
        "",
        "**Control Variable Files**:",
    ]

    for ctrl_tla in CONTROL_VARIABLE_TLAS:
        ctrl_path = RAW_DIR / f"{ctrl_tla}_raw.csv"
        if ctrl_path.exists():
            summary_lines.append(f"- {ctrl_tla}: `{ctrl_path}`")
        else:
            summary_lines.append(f"- {ctrl_tla}: NOT AVAILABLE")

    return "\n".join(summary_lines)
