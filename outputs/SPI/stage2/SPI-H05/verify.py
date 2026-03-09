import json
import os
import numpy as np
import pandas as pd

from src.utils.stats import (
    run_bivariate_correlation,
    run_partial_correlation,
    determine_verdict,
    build_result_json,
    test_functional_form,
)
from src.utils.data_utils import load_raw_indicator
from src.utils.data_fetch import fetch_world_bank_indicator

output_path = "/Users/samkouteili/rose/epi/multi-agent/outputs/SPI/stage2/SPI-H05"
os.makedirs(output_path, exist_ok=True)

print("=== SPI-H05: Terrestrial Protected Areas vs Species Protection Index ===\n")

# 1. Load EPI target data
print("Loading SPI target indicator...")
target = load_raw_indicator("SPI")
print(f"  SPI rows: {len(target)}, countries: {target['iso'].nunique()}")

# 2. Fetch proxy data from World Bank
print("\nFetching World Bank terrestrial protected areas data (ER.LND.PTLD.ZS)...")
try:
    proxy = fetch_world_bank_indicator("ER.LND.PTLD.ZS")
    proxy = proxy.rename(columns={"value": "proxy_value"})
    proxy = proxy.dropna(subset=["proxy_value"])
    print(f"  Proxy rows: {len(proxy)}, countries: {proxy['iso'].nunique()}")
    data_available = True
except Exception as e:
    print(f"  ERROR fetching proxy data: {e}")
    data_available = False

if not data_available:
    print("\nProxy data unavailable — writing inconclusive result.")
    result = {
        "hypothesis_id": "SPI-H05",
        "verdict": "inconclusive",
        "verification_method": "statistical_test",
        "data_quality_notes": (
            "Failed to fetch World Bank indicator ER.LND.PTLD.ZS "
            "(Terrestrial protected areas % of total land area). "
            "No alternative dataset was available."
        ),
        "summary": "Could not verify hypothesis due to data access failure.",
    }
    with open(f"{output_path}/result.json", "w") as f:
        json.dump(result, f, indent=2)
    print("Result written to result.json")
else:
    # 3. Merge on iso + year
    print("\nMerging SPI target with proxy data...")
    merged = target.merge(proxy, on=["iso", "year"])
    merged = merged.dropna(subset=["value", "proxy_value"])
    print(f"  Merged rows: {len(merged)}, countries: {merged['iso'].nunique()}")

    # 4. Bivariate correlation
    print("\nRunning bivariate correlation...")
    corr = run_bivariate_correlation(
        merged["proxy_value"], merged["value"], iso=merged["iso"]
    )
    print(f"  Pearson r={corr.pearson_r:.4f}, p={corr.pearson_p:.4e}")
    print(f"  Spearman rho={corr.spearman_rho:.4f}, p={corr.spearman_p:.4e}")
    print(f"  n_observations={corr.n_observations}, n_countries={corr.n_countries}")

    # 5. Partial correlation controlling for log(GDP per capita)
    print("\nLoading GPC for partial correlation control...")
    gpc = load_raw_indicator("GPC")
    merged_gpc = merged.merge(
        gpc[["iso", "year", "value"]].rename(columns={"value": "gpc"}),
        on=["iso", "year"],
    )
    merged_gpc = merged_gpc.dropna(subset=["gpc"])
    merged_gpc["log_gpc"] = np.log(merged_gpc["gpc"].clip(lower=1e-9))
    print(f"  Rows after GPC merge: {len(merged_gpc)}")

    print("Running partial correlation (controlling for log GDP per capita)...")
    partial = run_partial_correlation(
        merged_gpc, "proxy_value", "value", ["log_gpc"]
    )
    print(f"  Partial r={partial.partial_r:.4f}, p={partial.partial_p:.4e}")

    # 6. Functional form test
    print("\nTesting functional form (linear vs log-linear vs quadratic)...")
    form = test_functional_form(merged["proxy_value"], merged["value"])
    print(f"  Best form: {form.best_form.value}")

    # Helper to safely format potentially-None floats
    def fmt_r2(v):
        return f"{v:.4f}" if v is not None else "N/A"

    def fmt_aic(v):
        return f"{v:.2f}" if v is not None else "N/A"

    print(f"  Linear     R²={fmt_r2(form.linear_r2)}, AIC={fmt_aic(form.linear_aic)}")
    print(f"  Log-linear R²={fmt_r2(form.log_linear_r2)}, AIC={fmt_aic(form.log_linear_aic)}")
    print(f"  Quadratic  R²={fmt_r2(form.quadratic_r2)}, AIC={fmt_aic(form.quadratic_aic)}")

    # 7. Verdict
    print("\nDetermining verdict...")
    verdict = determine_verdict(corr, partial, "positive")
    print(f"  Verdict: {verdict.value}")

    # 8. Build and write result JSON
    best_form_str = form.best_form.value if form.best_form is not None else "unknown"

    result = build_result_json(
        "SPI-H05",
        verdict,
        corr,
        partial,
        functional_form=form,
        data_quality_notes=(
            "Proxy: World Bank ER.LND.PTLD.ZS — Terrestrial protected areas "
            "as % of total land area. Data covers 1992–2024. Includes all IUCN "
            "protected area categories; designation does not ensure effective "
            "management. No marine protected areas included. "
            "Note: log-linear functional form fit returned None (likely due to "
            "zero values in the proxy — some countries have 0% protected area). "
            f"Merged dataset: {len(merged)} obs, {merged['iso'].nunique()} countries."
        ),
        summary=(
            f"Terrestrial protected area percentage shows a "
            f"{'positive' if corr.pearson_r > 0 else 'negative'} correlation "
            f"with SPI (Pearson r={corr.pearson_r:.3f}, p={corr.pearson_p:.3e}; "
            f"Spearman rho={corr.spearman_rho:.3f}). "
            f"After controlling for log GDP per capita, partial r={partial.partial_r:.3f} "
            f"(p={partial.partial_p:.3e}). Best functional form: {best_form_str}. "
            f"Verdict: {verdict.value}."
        ),
    )
    result["verification_method"] = "statistical_test"

    out_file = f"{output_path}/result.json"
    with open(out_file, "w") as f:
        json.dump(result, f, indent=2)
    print(f"\nResult written to {out_file}")
    print(json.dumps(result, indent=2))