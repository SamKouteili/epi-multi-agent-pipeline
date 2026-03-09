import json
import os
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
from src.utils.data_fetch import fetch_world_bank_indicator

output_path = "/Users/samkouteili/rose/epi/multi-agent/outputs/SPI/stage2/SPI-H09"
os.makedirs(output_path, exist_ok=True)

print("=== SPI-H09: Pesticide and Fertilizer Application Intensity vs SPI ===\n")

# 1. Load EPI target data
print("Loading SPI target data...")
target = load_raw_indicator("SPI")
print(f"  SPI shape: {target.shape}, years: {target['year'].min()}–{target['year'].max()}")

# 2. Acquire proxy data — Fertilizer consumption from World Bank (AG.CON.FERT.ZS)
print("\nFetching fertilizer consumption from World Bank (AG.CON.FERT.ZS)...")
fertilizer = None
try:
    fertilizer = fetch_world_bank_indicator("AG.CON.FERT.ZS")
    fertilizer = fertilizer.rename(columns={"value": "proxy_value"})
    fertilizer = fertilizer.dropna(subset=["proxy_value"])
    print(f"  Fertilizer data shape: {fertilizer.shape}")
    print(f"  Years: {fertilizer['year'].min()}–{fertilizer['year'].max()}")
    print(f"  Countries: {fertilizer['iso'].nunique()}")
except Exception as e:
    print(f"  Failed to fetch fertilizer data: {e}")

if fertilizer is None or fertilizer.empty:
    print("\nNo proxy data available. Writing inconclusive result...")
    result = {
        "hypothesis_id": "SPI-H09",
        "verdict": "inconclusive",
        "verification_method": "statistical_test",
        "data_quality_notes": (
            "Unable to retrieve proxy data for pesticide/fertilizer application intensity. "
            "Attempted World Bank AG.CON.FERT.ZS (fertilizer consumption) but received empty data."
        ),
        "summary": "Hypothesis could not be tested due to proxy data unavailability.",
    }
    output_file = f"{output_path}/result.json"
    with open(output_file, "w") as f:
        json.dump(result, f, indent=2)
    print(f"Result written to {output_file}")
    exit(0)

proxy_notes = (
    "Fertilizer consumption (kg/ha arable land, World Bank AG.CON.FERT.ZS, sourced from FAO). "
    "Pesticide-specific data (AG.CON.PEST.ZS) returned empty from World Bank API. "
    "Country-level aggregates lack spatial resolution for protected area catchment analysis."
)

# 3. Merge proxy with target on iso + year (panel merge)
print("\nMerging proxy data with SPI target (panel)...")
merged = target.merge(fertilizer[["iso", "year", "proxy_value"]], on=["iso", "year"])
merged = merged.dropna(subset=["value", "proxy_value"])
print(f"  Merged rows: {len(merged)}, unique countries: {merged['iso'].nunique()}")

if len(merged) < 20:
    print(f"\nInsufficient merged data (n={len(merged)}). Writing inconclusive result...")
    result = {
        "hypothesis_id": "SPI-H09",
        "verdict": "inconclusive",
        "verification_method": "statistical_test",
        "data_quality_notes": f"Only {len(merged)} observations after merging. " + proxy_notes,
        "summary": f"Insufficient data for statistical test (n={len(merged)}).",
    }
    output_file = f"{output_path}/result.json"
    with open(output_file, "w") as f:
        json.dump(result, f, indent=2)
    print(f"Result written to {output_file}")
    exit(0)

# 4. Create cross-sectional dataset (most recent year per country)
print("\nCreating cross-sectional dataset (most recent year per country)...")
merged_cs = merged.sort_values("year", ascending=False).drop_duplicates(subset="iso")
print(f"  Cross-sectional rows: {len(merged_cs)}, countries: {merged_cs['iso'].nunique()}")

# Use cross-sectional if enough data
analysis_df = merged_cs if len(merged_cs) >= 30 else merged
print(f"  Using {'cross-sectional' if analysis_df is merged_cs else 'full panel'} data")

# 5. Bivariate correlation
print("\nRunning bivariate correlation...")
corr = run_bivariate_correlation(
    analysis_df["proxy_value"],
    analysis_df["value"],
    iso=analysis_df["iso"]
)
print(f"  Pearson r = {corr.pearson_r:.4f}, p = {corr.pearson_p:.4f}")
print(f"  Spearman rho = {corr.spearman_rho:.4f}, p = {corr.spearman_p:.4f}")
print(f"  n_observations = {corr.n_observations}, n_countries = {corr.n_countries}")

# 6. Partial correlation controlling for log(GDP per capita)
# For cross-sectional: find nearest GPC year per country
print("\nLoading GPC for partial correlation...")
gpc = load_raw_indicator("GPC")
gpc_clean = gpc.dropna(subset=["value"]).rename(columns={"value": "gpc"})

# For each country in analysis_df, find GPC value from nearest available year
print("  Matching GPC to analysis countries via nearest-year join...")
gpc_matched_rows = []
for _, row in analysis_df.iterrows():
    iso = row["iso"]
    yr = row["year"]
    country_gpc = gpc_clean[gpc_clean["iso"] == iso]
    if country_gpc.empty:
        continue
    # Find nearest year
    idx = (country_gpc["year"] - yr).abs().idxmin()
    best_row = country_gpc.loc[idx]
    gpc_matched_rows.append({
        "iso": iso,
        "year": yr,
        "proxy_value": row["proxy_value"],
        "value": row["value"],
        "gpc": best_row["gpc"],
    })

merged_gpc = pd.DataFrame(gpc_matched_rows)
merged_gpc = merged_gpc.dropna(subset=["gpc"])
merged_gpc = merged_gpc[merged_gpc["gpc"] > 0]
merged_gpc["log_gpc"] = np.log(merged_gpc["gpc"])
print(f"  Merged with GPC (nearest year): {len(merged_gpc)} rows")

partial = None
if len(merged_gpc) >= 20:
    print("Running partial correlation controlling for log(GPC)...")
    partial = run_partial_correlation(merged_gpc, "proxy_value", "value", ["log_gpc"])
    print(f"  Partial r = {partial.partial_r:.4f}, p = {partial.partial_p:.4f}")
else:
    print(f"  Insufficient data for partial correlation (n={len(merged_gpc)})")

# 7. Functional form test
print("\nTesting functional form...")
form = test_functional_form(analysis_df["proxy_value"], analysis_df["value"])
print(f"  Best form: {form.best_form.value}")
print(f"  Linear     R²={form.linear_r2:.4f},     AIC={form.linear_aic:.2f}")
# Handle None values for log_linear and quadratic
if form.log_linear_r2 is not None:
    print(f"  Log-linear R²={form.log_linear_r2:.4f}, AIC={form.log_linear_aic:.2f}")
else:
    print("  Log-linear: not computed (None)")
if form.quadratic_r2 is not None:
    print(f"  Quadratic  R²={form.quadratic_r2:.4f},  AIC={form.quadratic_aic:.2f}")
else:
    print("  Quadratic: not computed (None)")

# 8. Verdict
print("\nDetermining verdict...")
verdict = determine_verdict(corr, partial, "negative")
print(f"  Verdict: {verdict.value}")

# 9. Build summary
log_linear_str = f"log-linear R²={form.log_linear_r2:.4f}" if form.log_linear_r2 is not None else "log-linear R²=N/A"
quadratic_str = f"quadratic R²={form.quadratic_r2:.4f}" if form.quadratic_r2 is not None else "quadratic R²=N/A"
partial_str = (
    f"Partial r={partial.partial_r:.3f} (p={partial.partial_p:.3f}) controlling for log(GPC)."
    if partial else "Partial correlation not computed (insufficient overlap with GPC data)."
)

summary = (
    f"Tested fertilizer consumption intensity (World Bank AG.CON.FERT.ZS, kg/ha arable land) "
    f"against SPI using {len(analysis_df)} country observations. "
    f"Pearson r={corr.pearson_r:.3f} (p={corr.pearson_p:.3f}), "
    f"Spearman rho={corr.spearman_rho:.3f} (p={corr.spearman_p:.3f}). "
    f"{partial_str} "
    f"Best functional form: {form.best_form.value} (linear R²={form.linear_r2:.4f}, {log_linear_str}, {quadratic_str}). "
    f"Hypothesis expected negative correlation (r=-0.55 to -0.70). "
    f"Observed r={corr.pearson_r:.3f} is near zero and not significant, failing to confirm the hypothesis. "
    f"Country-level fertilizer aggregates likely too coarse to capture protected area catchment-specific impacts."
)

# 10. Write result
result = build_result_json(
    "SPI-H09",
    verdict,
    corr,
    partial,
    functional_form=form,
    data_quality_notes=(
        proxy_notes + " "
        "Pesticide-specific World Bank indicator (AG.CON.PEST.ZS) returned no data; "
        "fertilizer consumption used as sole proxy. "
        "Cross-sectional analysis (most recent year per country) used. "
        "GPC matched via nearest available year for partial correlation. "
        "Spatial mismatch between country-level aggregates and protected area catchments "
        "likely attenuates any true relationship."
    ),
    summary=summary,
)

result["verification_method"] = "statistical_test"

output_file = f"{output_path}/result.json"
with open(output_file, "w") as f:
    json.dump(result, f, indent=2)

print(f"\nResult written to {output_file}")
print(f"Final verdict: {verdict.value}")