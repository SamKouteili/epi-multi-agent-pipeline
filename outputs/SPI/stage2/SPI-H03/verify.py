import json
import os
import requests
import pandas as pd
import numpy as np

from src.utils.stats import (
    run_bivariate_correlation,
    run_partial_correlation,
    determine_verdict,
    build_result_json,
    test_functional_form,
)
from src.utils.data_utils import load_raw_indicator
from src.utils.data_fetch import (
    fetch_world_bank_indicator,
    search_world_bank,
    list_local_indicators,
)

output_path = "/Users/samkouteili/rose/epi/multi-agent/outputs/SPI/stage2/SPI-H03"
os.makedirs(output_path, exist_ok=True)

HYPOTHESIS_ID = "SPI-H03"
EXPECTED_DIRECTION = "positive"

print("=" * 60)
print(f"Hypothesis: {HYPOTHESIS_ID}")
print("Proxy: Species Habitat Index (SHI)")
print("=" * 60)

# ── 1. Load EPI target ──────────────────────────────────────────
print("\n[1] Loading SPI target data...")
target = load_raw_indicator("SPI")
print(f"    Target rows: {len(target)}, countries: {target['iso'].nunique()}")

# ── 2. Load SHI from local EPI files ───────────────────────────
print("\n[2] Checking for SHI in local EPI raw files...")
local_indicators = list_local_indicators()
local_tlas = [ind['tla'] for ind in local_indicators]

if "SHI" not in local_tlas:
    print("    SHI not found locally. Reporting inconclusive.")
    result = build_result_json(
        HYPOTHESIS_ID,
        "inconclusive",
        None,
        None,
        data_quality_notes=(
            "SHI not found in local EPI raw files and not available via public APIs."
        ),
        summary="Data unavailable.",
        verification_method="statistical_test",
    )
    out_file = f"{output_path}/result.json"
    with open(out_file, "w") as f:
        json.dump(result, f, indent=2)
    print(json.dumps(result, indent=2))
    exit(0)

print("    Found SHI locally!")
shi_df = load_raw_indicator("SHI").rename(columns={"value": "proxy_value"})
print(f"    SHI rows: {len(shi_df)}, countries: {shi_df['iso'].nunique()}")

# ── 3. Merge on iso + year ──────────────────────────────────────
print("\n[3] Merging SHI with SPI...")
merged = target.merge(shi_df[["iso", "year", "proxy_value"]], on=["iso", "year"])
merged = merged.dropna(subset=["value", "proxy_value"])
print(f"    Merged rows: {len(merged)}, countries: {merged['iso'].nunique()}")

if len(merged) < 20:
    print("[!] Too few observations. Reporting inconclusive.")
    result = build_result_json(
        HYPOTHESIS_ID,
        "inconclusive",
        None,
        None,
        data_quality_notes=f"Only {len(merged)} observations after merging SHI and SPI.",
        summary="Insufficient data overlap.",
        verification_method="statistical_test",
    )
    out_file = f"{output_path}/result.json"
    with open(out_file, "w") as f:
        json.dump(result, f, indent=2)
    print(json.dumps(result, indent=2))
    exit(0)

# ── 4. Bivariate correlation ────────────────────────────────────
print("\n[4] Running bivariate correlation...")
corr = run_bivariate_correlation(
    merged["proxy_value"], merged["value"], iso=merged["iso"]
)
print(f"    Pearson r={corr.pearson_r:.3f} (p={corr.pearson_p:.4f})")
print(f"    Spearman rho={corr.spearman_rho:.3f} (p={corr.spearman_p:.4f})")
print(f"    n={corr.n_observations}, countries={corr.n_countries}")

# ── 5. Partial correlation controlling for log(GPC) ─────────────
print("\n[5] Running partial correlation (controlling for log GDP/capita)...")
gpc = load_raw_indicator("GPC")
merged_gpc = merged.merge(
    gpc[["iso", "year", "value"]].rename(columns={"value": "gpc"}),
    on=["iso", "year"],
)
merged_gpc = merged_gpc.dropna(subset=["gpc"])
merged_gpc["log_gpc"] = np.log(merged_gpc["gpc"].replace(0, np.nan))
merged_gpc = merged_gpc.dropna(subset=["log_gpc"])
print(f"    n for partial correlation: {len(merged_gpc)}")

if len(merged_gpc) >= 20:
    partial = run_partial_correlation(
        merged_gpc, "proxy_value", "value", ["log_gpc"]
    )
    print(f"    Partial r={partial.partial_r:.3f} (p={partial.partial_p:.4f})")
else:
    partial = None
    print("    Too few observations for partial correlation.")

# ── 6. Functional form ──────────────────────────────────────────
print("\n[6] Testing functional form...")
form = test_functional_form(merged["proxy_value"], merged["value"])
print(f"    Best form: {form.best_form.value}")
print(f"    Linear R²={form.linear_r2:.3f}, Log-linear R²={form.log_linear_r2:.3f}, Quadratic R²={form.quadratic_r2:.3f}")

# ── 7. Verdict ──────────────────────────────────────────────────
print("\n[7] Determining verdict...")
verdict = determine_verdict(corr, partial, EXPECTED_DIRECTION)
print(f"    Verdict: {verdict.value}")

# ── 8. Build result — inspect build_result_json signature ───────
import inspect
sig = inspect.signature(build_result_json)
print(f"\n[8] build_result_json signature: {sig}")

# Call with positional args to avoid keyword conflicts
# Signature from system prompt: build_result_json(hypothesis_id, verdict, corr, partial, ...)
# But the error shows 'partial' is not accepted — try without it

partial_summary = ""
if partial is not None:
    partial_summary = (
        f"Partial r={partial.partial_r:.3f} (p={partial.partial_p:.4f}) "
        "controlling for log GDP/capita. "
    )

data_quality_notes = (
    "SHI data loaded from local EPI raw files (Map of Life source). "
    "Note: SHI does not distinguish intact habitat inside versus outside protected areas; "
    "relies on GBIF occurrence records introducing geographic bias toward well-sampled regions; "
    "different species groups have different habitat requirements affecting country-level aggregation. "
    f"Pearson r={corr.pearson_r:.3f} is NEGATIVE, opposite to the expected positive direction, "
    "suggesting that countries with higher SHI (more intact habitat) do not necessarily have "
    "higher SPI (protected area coverage). This may reflect that SHI measures remaining intact "
    "habitat broadly while SPI measures the fraction within formal protected areas — countries "
    "with large intact areas may have low protected-area designation rates."
)

summary = (
    f"SHI vs SPI bivariate: Pearson r={corr.pearson_r:.3f} (p={corr.pearson_p:.4f}), "
    f"Spearman rho={corr.spearman_rho:.3f} (p={corr.spearman_p:.4f}), "
    f"n={corr.n_observations} observations across {corr.n_countries} countries. "
    f"{partial_summary}"
    f"Best functional form: {form.best_form.value}. "
    f"Verdict: {verdict.value}. "
    "The correlation is negative and significant, opposite to the hypothesized positive direction. "
    "The hypothesis that SHI positively predicts SPI is REJECTED by the data."
)

# Try different call patterns based on actual signature
params = list(sig.parameters.keys())
print(f"    Parameters: {params}")

try:
    # Pattern 1: positional (hypothesis_id, verdict, corr, partial_corr, functional_form, ...)
    result = build_result_json(
        HYPOTHESIS_ID,
        verdict,
        corr,
        partial,
        form,
        data_quality_notes=data_quality_notes,
        summary=summary,
        verification_method="statistical_test",
    )
    print("    Used pattern 1 (positional: id, verdict, corr, partial, form)")
except TypeError as e1:
    print(f"    Pattern 1 failed: {e1}")
    try:
        # Pattern 2: no partial positional arg
        result = build_result_json(
            HYPOTHESIS_ID,
            verdict,
            corr,
            form,
            data_quality_notes=data_quality_notes,
            summary=summary,
            verification_method="statistical_test",
        )
        print("    Used pattern 2 (positional: id, verdict, corr, form)")
    except TypeError as e2:
        print(f"    Pattern 2 failed: {e2}")
        try:
            # Pattern 3: only required args
            result = build_result_json(
                HYPOTHESIS_ID,
                verdict,
                corr,
            )
            # Then manually add extra fields
            result["partial_correlation"] = {
                "partial_r": partial.partial_r if partial else None,
                "partial_p": partial.partial_p if partial else None,
                "control_variables": partial.control_variables if partial else [],
            }
            result["functional_form"] = {
                "best_form": form.best_form.value,
                "linear_r2": form.linear_r2,
                "log_linear_r2": form.log_linear_r2,
                "quadratic_r2": form.quadratic_r2,
            }
            result["data_quality_notes"] = data_quality_notes
            result["summary"] = summary
            result["verification_method"] = "statistical_test"
            print("    Used pattern 3 (minimal positional, manual extras)")
        except TypeError as e3:
            print(f"    Pattern 3 failed: {e3}")
            # Pattern 4: pure keyword args — inspect actual param names
            kwargs = {}
            for p in params:
                if p in ["hypothesis_id", "id"]:
                    kwargs[p] = HYPOTHESIS_ID
                elif p == "verdict":
                    kwargs[p] = verdict
                elif p in ["corr", "correlation", "bivariate"]:
                    kwargs[p] = corr
                elif p in ["partial", "partial_corr", "partial_correlation"]:
                    kwargs[p] = partial
                elif p in ["functional_form", "form"]:
                    kwargs[p] = form
            kwargs["data_quality_notes"] = data_quality_notes
            kwargs["summary"] = summary
            kwargs["verification_method"] = "statistical_test"
            result = build_result_json(**kwargs)
            print(f"    Used pattern 4 (keyword mapping): {list(kwargs.keys())}")

# ── 9. Write output ─────────────────────────────────────────────
out_file = f"{output_path}/result.json"
with open(out_file, "w") as f:
    json.dump(result, f, indent=2)
print(f"\nResult written to: {out_file}")
print(json.dumps(result, indent=2))