import json
import os
import pandas as pd
import numpy as np
import requests

from src.utils.stats import (
    run_bivariate_correlation,
    run_partial_correlation,
    determine_verdict,
    build_result_json,
    test_functional_form,
)
from src.utils.data_utils import load_raw_indicator
from src.utils.data_fetch import fetch_world_bank_indicator, search_world_bank

output_path = "/Users/samkouteili/rose/epi/multi-agent/outputs/WRR/stage2/WRR-H10"
os.makedirs(output_path, exist_ok=True)

print("=" * 60)
print("WRR-H10: Landfill Gas Recovery Capacity vs WRR")
print("=" * 60)

# 1. Load EPI target data
print("\n[1] Loading WRR target indicator...")
target = load_raw_indicator("WRR")
print(f"    WRR shape: {target.shape}")
print(f"    Years: {sorted(target['year'].unique())}")
print(f"    Countries: {target['iso'].nunique()}")

# 2. Acquire proxy data
# The EPA LMOP data is US-only; we use World Bank waste/energy indicators as proxies
# for landfill gas recovery capacity. We try multiple WB indicators.

print("\n[2] Attempting to acquire proxy data...")

proxy_df = None
proxy_source_note = ""

# Try WB indicators in order of relevance
wb_indicators_to_try = [
    ("EG.ELC.RNWX.KH", "Renewable electricity capacity excl hydro (MW)"),
    ("EG.ELC.RNWX.ZS", "Renewable electricity output excl hydro % of total"),
    ("EN.ATM.METH.KT.CE", "Total methane emissions"),
    ("EG.USE.PCAP.KG.OE", "Energy use per capita (kg oil equivalent)"),
    ("EG.ELC.FOSL.ZS", "Electricity production from oil/gas/coal"),
]

for wb_code, wb_desc in wb_indicators_to_try:
    print(f"\n    Trying WB indicator: {wb_code} ({wb_desc})...")
    try:
        df = fetch_world_bank_indicator(wb_code)
        if df is not None and len(df) > 100:
            proxy_df = df.rename(columns={"value": "proxy_value"})
            proxy_source_note = f"World Bank: {wb_desc} ({wb_code})"
            print(f"    SUCCESS: {len(proxy_df)} rows, {proxy_df['iso'].nunique()} countries")
            break
        else:
            print(f"    Insufficient data (returned {len(df) if df is not None else 0} rows)")
    except Exception as e:
        print(f"    Failed: {e}")

# 3. Process proxy data if we have it
if proxy_df is not None:
    print(f"\n[3] Processing proxy data: {proxy_source_note}")
    print(f"    Proxy shape: {proxy_df.shape}")

    # Merge on iso + year
    merged = target.merge(proxy_df[["iso", "year", "proxy_value"]], on=["iso", "year"])
    print(f"    Merged shape: {merged.shape}")
    print(f"    Merged countries: {merged['iso'].nunique()}")

    # Drop NAs
    merged = merged.dropna(subset=["proxy_value", "value"])
    print(f"    After dropna: {merged.shape}, {merged['iso'].nunique()} countries")

    if len(merged) < 20:
        print("    WARNING: Insufficient observations after merge — setting inconclusive")
        proxy_df = None

if proxy_df is not None:
    # 4. Bivariate correlation
    print("\n[4] Running bivariate correlation...")
    corr = run_bivariate_correlation(
        merged["proxy_value"], merged["value"], iso=merged["iso"]
    )
    print(f"    Pearson r={corr.pearson_r:.4f}, p={corr.pearson_p:.4f}")
    print(f"    Spearman rho={corr.spearman_rho:.4f}, p={corr.spearman_p:.4f}")
    print(f"    n={corr.n_observations}, countries={corr.n_countries}")

    # 5. Partial correlation controlling for log(GDP per capita)
    print("\n[5] Running partial correlation (controlling for log GPC)...")
    gpc = load_raw_indicator("GPC")
    merged_gpc = merged.merge(
        gpc[["iso", "year", "value"]].rename(columns={"value": "gpc"}),
        on=["iso", "year"],
    )
    merged_gpc = merged_gpc.dropna(subset=["gpc", "proxy_value", "value"])
    merged_gpc["log_gpc"] = np.log(merged_gpc["gpc"].clip(lower=1e-9))
    print(f"    Merged with GPC: {merged_gpc.shape}, {merged_gpc['iso'].nunique()} countries")

    partial = None
    if len(merged_gpc) >= 20:
        # Check for near-perfect collinearity or degenerate cases before running
        proxy_std = merged_gpc["proxy_value"].std()
        value_std = merged_gpc["value"].std()
        log_gpc_std = merged_gpc["log_gpc"].std()
        print(f"    Stdev check — proxy: {proxy_std:.4f}, value: {value_std:.4f}, log_gpc: {log_gpc_std:.4f}")

        if proxy_std > 1e-6 and value_std > 1e-6 and log_gpc_std > 1e-6:
            try:
                partial = run_partial_correlation(
                    merged_gpc, "proxy_value", "value", ["log_gpc"]
                )
                print(f"    Partial r={partial.partial_r:.4f}, p={partial.partial_p:.4f}")
            except Exception as e:
                print(f"    Partial correlation failed: {e}")
                print("    Continuing without partial correlation.")
                partial = None
        else:
            print("    Skipping partial correlation — near-zero variance in one or more variables.")
    else:
        print("    Insufficient data for partial correlation")

    # 6. Functional form test
    print("\n[6] Testing functional forms...")
    # Use log of proxy (capacity is likely log-related)
    proxy_vals = merged["proxy_value"].copy()
    # Clip to positive values for log transform
    proxy_positive = proxy_vals[proxy_vals > 0]
    value_positive = merged.loc[proxy_vals > 0, "value"]
    
    if len(proxy_positive) >= 20:
        form = test_functional_form(proxy_positive, value_positive)
        print(f"    Best form: {form.best_form.value}")
        print(f"    Linear R²={form.linear_r2:.4f}, AIC={form.linear_aic:.2f}")
        print(f"    Log-linear R²={form.log_linear_r2:.4f}, AIC={form.log_linear_aic:.2f}")
        print(f"    Quadratic R²={form.quadratic_r2:.4f}, AIC={form.quadratic_aic:.2f}")
    else:
        form = test_functional_form(merged["proxy_value"], merged["value"])
        print(f"    Best form: {form.best_form.value}")

    # 7. Verdict
    print("\n[7] Determining verdict...")
    verdict = determine_verdict(corr, partial, "positive")
    print(f"    Verdict: {verdict.value}")

    # Build partial summary string
    if partial is not None:
        partial_summary = (
            f"Partial r={partial.partial_r:.3f} (p={partial.partial_p:.3f}) "
            f"after controlling for log(GDP/capita). "
        )
    else:
        partial_summary = "Partial correlation could not be computed. "

    # Build result
    result = build_result_json(
        "WRR-H10",
        verdict,
        corr,
        partial,
        functional_form=form,
        data_quality_notes=(
            f"Proxy used: {proxy_source_note}. "
            "The hypothesis specified EPA LMOP Landfill Gas Recovery Capacity data, "
            "which is US-only and not available as a global dataset. "
            "As a global substitute we used a World Bank energy/renewables indicator. "
            "This is an imperfect proxy for LFG recovery capacity specifically, "
            "but captures broader energy infrastructure that correlates with waste "
            "management sophistication. "
            "Two WB methane indicators (EN.ATM.METH.EG.KT.CE, EN.ATM.METH.PC) "
            "returned no valid data (invalid WB codes). "
            "Partial correlation was attempted but may have been skipped due to "
            "numerical issues (near-zero variance or degenerate pingouin output)."
        ),
        summary=(
            f"Testing whether {proxy_source_note} correlates with WRR (waste recovery rate). "
            f"Bivariate: Pearson r={corr.pearson_r:.3f} (p={corr.pearson_p:.3f}), "
            f"Spearman rho={corr.spearman_rho:.3f} (p={corr.spearman_p:.3f}), "
            f"n={corr.n_observations} observations, {corr.n_countries} countries. "
            + partial_summary
            + f"Best functional form: {form.best_form.value}. "
            f"Verdict: {verdict.value}. "
            "Note: proxy is a broad energy indicator, not directly LFG-specific."
        ),
    )
    result["verification_method"] = "statistical_test"

else:
    # Inconclusive fallback
    print("\n[INCONCLUSIVE] No suitable proxy data found or insufficient observations.")
    result = {
        "hypothesis_id": "WRR-H10",
        "verdict": "inconclusive",
        "verification_method": "statistical_test",
        "data_quality_notes": (
            "The primary data source specified (EPA LMOP — Landfill Methane Outreach Program) "
            "covers only the United States comprehensively and is not available as a global "
            "cross-country dataset suitable for EPI analysis. "
            "Attempts to find a suitable World Bank substitute indicator for landfill "
            "gas recovery capacity globally were unsuccessful — either the data was unavailable "
            "or had insufficient country coverage after merging with WRR data. "
            "World Bank methane emission indicators were tried (EN.ATM.METH.EG.KT.CE, "
            "EN.ATM.METH.PC) but returned invalid/empty responses. "
            "Additional WB indicators (EG.ELC.RNWX.KH, EG.ELC.RNWX.ZS, EN.ATM.METH.KT.CE, "
            "EG.USE.PCAP.KG.OE, EG.ELC.FOSL.ZS) were tried as fallbacks. "
            "If all fail to merge with sufficient WRR observations, the hypothesis "
            "cannot be statistically verified without a global LFG dataset."
        ),
        "summary": (
            "Hypothesis WRR-H10 tests whether landfill gas (LFG) recovery capacity "
            "correlates positively with WRR (waste recovery rate). The EPA LMOP database "
            "is the canonical source but is US-only. No suitable global proxy dataset "
            "with sufficient coverage was found. Verdict: inconclusive."
        ),
        "bivariate_correlation": None,
        "partial_correlation": None,
        "functional_form": None,
    }

# 8. Write output
output_file = f"{output_path}/result.json"
with open(output_file, "w") as f:
    json.dump(result, f, indent=2, default=str)

print(f"\n[8] Results written to: {output_file}")
print(f"    Final verdict: {result.get('verdict', 'N/A')}")
print("=" * 60)
print("Done.")