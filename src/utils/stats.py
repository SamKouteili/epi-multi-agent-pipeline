"""Shared statistical analysis functions for Stage 2 hypothesis verification."""

from __future__ import annotations

import math
from typing import Optional

import numpy as np
import pandas as pd
from scipy import stats as sp_stats

from src.config import (
    VERDICT_MIN_N,
    VERDICT_P_BORDERLINE,
    VERDICT_P_THRESHOLD,
    VERDICT_R_THRESHOLD,
    VERDICT_R_STRONG,
    VERDICT_P_STRICT,
    PARTIAL_CORR_MIN_N,
)
from src.schemas import (
    CorrelationResult,
    FunctionalForm,
    FunctionalFormResult,
    PartialCorrelationResult,
    Verdict,
)


def run_bivariate_correlation(
    x: pd.Series,
    y: pd.Series,
    iso: Optional[pd.Series] = None,
) -> CorrelationResult:
    """Compute Pearson and Spearman correlations between two series.

    Args:
        x: Proxy variable values.
        y: EPI indicator values.
        iso: Optional ISO3 codes for counting unique countries.

    Returns:
        CorrelationResult with r, rho, p-values, and observation counts.
    """
    mask = x.notna() & y.notna()
    x_clean, y_clean = x[mask].astype(float), y[mask].astype(float)
    n = len(x_clean)

    if n < 3:
        return CorrelationResult(n_observations=n, n_countries=0)

    pearson_r, pearson_p = sp_stats.pearsonr(x_clean, y_clean)
    spearman_rho, spearman_p = sp_stats.spearmanr(x_clean, y_clean)

    n_countries = int(iso[mask].nunique()) if iso is not None else None

    return CorrelationResult(
        pearson_r=float(pearson_r),
        pearson_p=float(pearson_p),
        spearman_rho=float(spearman_rho),
        spearman_p=float(spearman_p),
        n_observations=n,
        n_countries=n_countries,
    )


def run_partial_correlation(
    df: pd.DataFrame,
    x_col: str,
    y_col: str,
    covar_cols: list[str],
) -> Optional[PartialCorrelationResult]:
    """Compute partial correlation controlling for covariates.

    Uses pingouin.partial_corr. Returns None if fewer than
    PARTIAL_CORR_MIN_N complete observations.

    Args:
        df: DataFrame containing all columns.
        x_col: Name of the proxy variable column.
        y_col: Name of the EPI indicator column.
        covar_cols: Names of control variable columns (e.g. ["log_GPC"]).

    Returns:
        PartialCorrelationResult or None if insufficient data.
    """
    cols = [x_col, y_col] + covar_cols
    sub = df[cols].dropna()

    if len(sub) < PARTIAL_CORR_MIN_N:
        return None

    import pingouin as pg

    result = pg.partial_corr(data=sub, x=x_col, y=y_col, covar=covar_cols)

    return PartialCorrelationResult(
        partial_r=float(result["r"].iloc[0]),
        partial_p=float(result["p-val"].iloc[0]),
        control_variables=list(covar_cols),
    )


def test_functional_form(
    x: pd.Series,
    y: pd.Series,
    min_n: int = 20,
) -> Optional[FunctionalFormResult]:
    """Test linear, log-linear, and quadratic fits via AIC comparison.

    Args:
        x: Proxy variable values.
        y: EPI indicator values.
        min_n: Minimum observations required.

    Returns:
        FunctionalFormResult with R² and AIC for each model, or None if < min_n observations.
    """
    mask = x.notna() & y.notna()
    xc, yc = x[mask].astype(float).values, y[mask].astype(float).values
    n = len(xc)

    if n < min_n:
        return None

    def _aic(rss: float, n: int, k: int) -> float:
        """AIC = n·ln(RSS/n) + 2k."""
        return n * np.log(rss / n) + 2 * k

    def _r2(y_true: np.ndarray, y_pred: np.ndarray) -> float:
        ss_res = np.sum((y_true - y_pred) ** 2)
        ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)
        if ss_tot == 0:
            return 0.0
        return float(1.0 - ss_res / ss_tot)

    candidates: list[tuple[FunctionalForm, float, float]] = []  # (form, r2, aic)

    # Linear: y = a + bx (k=2)
    coeffs = np.polyfit(xc, yc, 1)
    y_pred = np.polyval(coeffs, xc)
    rss = float(np.sum((yc - y_pred) ** 2))
    lin_r2 = _r2(yc, y_pred)
    lin_aic = _aic(rss, n, 2)
    candidates.append((FunctionalForm.linear, lin_r2, lin_aic))

    # Log-linear: y = a + b·ln(x) (k=2), only if all x > 0
    log_r2: Optional[float] = None
    log_aic: Optional[float] = None
    if np.all(xc > 0):
        log_x = np.log(xc)
        coeffs = np.polyfit(log_x, yc, 1)
        y_pred = np.polyval(coeffs, log_x)
        rss = float(np.sum((yc - y_pred) ** 2))
        log_r2 = _r2(yc, y_pred)
        log_aic = _aic(rss, n, 2)
        candidates.append((FunctionalForm.log_linear, log_r2, log_aic))

    # Quadratic: y = a + bx + cx² (k=3)
    coeffs = np.polyfit(xc, yc, 2)
    y_pred = np.polyval(coeffs, xc)
    rss = float(np.sum((yc - y_pred) ** 2))
    quad_r2 = _r2(yc, y_pred)
    quad_aic = _aic(rss, n, 3)
    candidates.append((FunctionalForm.quadratic, quad_r2, quad_aic))

    # Select best by lowest AIC (prefer simpler on ties)
    best_form = min(candidates, key=lambda t: t[2])[0]

    return FunctionalFormResult(
        best_form=best_form,
        linear_r2=lin_r2,
        linear_aic=lin_aic,
        log_linear_r2=log_r2,
        log_linear_aic=log_aic,
        quadratic_r2=quad_r2,
        quadratic_aic=quad_aic,
    )


def determine_verdict(
    corr: CorrelationResult,
    partial_corr: Optional[PartialCorrelationResult],
    expected_direction: str,
) -> Verdict:
    """Determine hypothesis verdict from correlation results.

    Decision tree:
        1. n < MIN_N → inconclusive
        2. Direction mismatch → rejected
        3. p > BORDERLINE → rejected
        4. THRESHOLD < p ≤ BORDERLINE → inconclusive
        5. |r| > R_THRESHOLD & p < THRESHOLD & partial significant → confirmed
        6. |r| > R_THRESHOLD & p < THRESHOLD & partial not significant → partially_confirmed
        7. Else → partially_confirmed

    Args:
        corr: Bivariate correlation result.
        partial_corr: Partial correlation result (may be None).
        expected_direction: One of "positive", "negative", "nonlinear", "unknown".

    Returns:
        Verdict enum value.
    """
    n = corr.n_observations or 0
    r = corr.pearson_r
    p = corr.pearson_p

    # 1. Insufficient data
    if n < VERDICT_MIN_N:
        return Verdict.inconclusive

    if r is None or p is None:
        return Verdict.inconclusive

    # 2. Direction mismatch
    if expected_direction == "positive" and r < 0:
        return Verdict.rejected
    if expected_direction == "negative" and r > 0:
        return Verdict.rejected

    # 3. Not significant at all
    if p > VERDICT_P_BORDERLINE:
        return Verdict.rejected

    # 4. Borderline significance
    if p > VERDICT_P_THRESHOLD:
        return Verdict.inconclusive

    # 5–7. Significant (p < THRESHOLD)
    if abs(r) > VERDICT_R_THRESHOLD:
        # Check partial correlation
        if partial_corr is not None and partial_corr.partial_p is not None:
            if partial_corr.partial_p < VERDICT_P_THRESHOLD:
                return Verdict.confirmed
            else:
                return Verdict.partially_confirmed
        # Partial correlation not available — use stricter bivariate thresholds
        if abs(r) > VERDICT_R_STRONG and p < VERDICT_P_STRICT:
            return Verdict.confirmed
        return Verdict.partially_confirmed

    # Significant p but weak effect size
    return Verdict.partially_confirmed


def build_result_json(
    hypothesis_id: str,
    verdict: Verdict,
    corr: CorrelationResult,
    partial_corr: Optional[PartialCorrelationResult] = None,
    functional_form: Optional[FunctionalFormResult] = None,
    data_quality_notes: str = "",
    summary: str = "",
    verification_method: Optional[str] = None,
) -> dict:
    """Build the result.json dict matching VerificationResult schema.

    Args:
        hypothesis_id: e.g. "UWD-H01".
        verdict: Determined verdict.
        corr: Bivariate correlation result.
        partial_corr: Partial correlation result (may be None).
        functional_form: Functional form test result (may be None).
        data_quality_notes: Notes about data quality issues.
        summary: Human-readable summary of findings.
        verification_method: How the hypothesis was verified (e.g. "statistical_test").

    Returns:
        dict ready to be serialized to JSON.
    """

    def _clean(v):
        """Replace NaN/Inf with None for JSON serialization."""
        if v is None:
            return None
        if isinstance(v, float) and (math.isnan(v) or math.isinf(v)):
            return None
        return v

    result = {
        "hypothesis_id": hypothesis_id,
        "verdict": verdict.value,
        "verification_method": verification_method,
        "raw_correlation": {
            "pearson_r": _clean(corr.pearson_r),
            "pearson_p": _clean(corr.pearson_p),
            "spearman_rho": _clean(corr.spearman_rho),
            "spearman_p": _clean(corr.spearman_p),
            "n_observations": corr.n_observations,
            "n_countries": corr.n_countries,
        },
        "partial_correlation": None,
        "functional_form": None,
        "data_quality_notes": data_quality_notes,
        "summary": summary,
    }

    if partial_corr is not None:
        result["partial_correlation"] = {
            "partial_r": _clean(partial_corr.partial_r),
            "partial_p": _clean(partial_corr.partial_p),
            "control_variables": partial_corr.control_variables,
        }

    if functional_form is not None:
        result["functional_form"] = {
            "best_form": functional_form.best_form.value,
            "linear_r2": _clean(functional_form.linear_r2),
            "linear_aic": _clean(functional_form.linear_aic),
            "log_linear_r2": _clean(functional_form.log_linear_r2),
            "log_linear_aic": _clean(functional_form.log_linear_aic),
            "quadratic_r2": _clean(functional_form.quadratic_r2),
            "quadratic_aic": _clean(functional_form.quadratic_aic),
        }

    return result
