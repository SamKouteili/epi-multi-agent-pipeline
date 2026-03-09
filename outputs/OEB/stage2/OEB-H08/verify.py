import json
import os
import pandas as pd
import numpy as np
import requests
import io

from src.utils.stats import (
    run_bivariate_correlation,
    run_partial_correlation,
    determine_verdict,
    build_result_json,
    test_functional_form,
)
from src.utils.data_utils import load_raw_indicator
from src.utils.data_fetch import fetch_world_bank_indicator, search_world_bank

output_path = "/Users/samkouteili/rose/epi/multi-agent/outputs/OEB/stage2/OEB-H08"
os.makedirs(output_path, exist_ok=True)

print("=== OEB-H08: Crop Yield Reductions as Proxy for Ozone Exposure ===")

# 1. Load EPI target data
print("\n[1] Loading OEB target indicator...")
target = load_raw_indicator("OEB")
print(f"    Target rows: {len(target)}, unique countries: {target['iso'].nunique()}")
print(f"    Year range: {target['year'].min()} - {target['year'].max()}")

# 2. Acquire proxy data — crop yields for ozone-sensitive crops from FAO via World Bank
# Ozone-sensitive crops: wheat, soybeans, maize
# Try World Bank indicators for crop yields (from FAO data)
# AG.YLD.CREL.KG = Cereal yield (kg per hectare)
# Wheat: AG.YLD.WHEA.KG, Soybean: we'll try multiple

print("\n[2] Fetching crop yield data from World Bank (FAO-sourced)...")

proxy_df = None
wb_indicators = {
    "cereal_yield": "AG.YLD.CREL.KG",   # Cereal yield (kg/ha) - broad ozone-sensitive category
    "wheat_yield": "AG.YLD.WHEA.KG",     # Wheat yield (kg/ha) - very ozone-sensitive
}

# Try cereal yield first (broadest coverage, ozone-sensitive)
for name, code in wb_indicators.items():
    print(f"    Trying World Bank indicator: {code} ({name})...")
    try:
        df = fetch_world_bank_indicator(code)
        if df is not None and len(df) > 100:
            df = df.rename(columns={"value": "proxy_value"})
            df["proxy_value"] = pd.to_numeric(df["proxy_value"], errors="coerce")
            df = df.dropna(subset=["proxy_value"])
            print(f"    Got {len(df)} rows, {df['iso'].nunique()} countries, years {df['year'].min()}-{df['year'].max()}")
            proxy_df = df
            proxy_indicator_used = f"World Bank {code} ({name})"
            break
    except Exception as e:
        print(f"    Failed: {e}")

# If World Bank fails, try searching for alternatives
if proxy_df is None:
    print("    Searching World Bank for crop yield indicators...")
    try:
        results = search_world_bank("cereal yield crop")
        print(f"    Search results: {results[:5] if results else 'None'}")
    except Exception as e:
        print(f"    Search failed: {e}")

# If still no data, try downloading from Our World in Data / FAO
if proxy_df is None:
    print("    Trying Our World in Data CSV download...")
    urls_to_try = [
        "https://raw.githubusercontent.com/owid/owid-datasets/master/datasets/Long-run%20cereal%20yields%20-%20Bayliss-Smith%20%26%20Wanmali%20(1984)%2C%20and%20FAO%20(2017)/Long-run%20cereal%20yields%20-%20Bayliss-Smith%20%26%20Wanmali%20(1984)%2C%20and%20FAO%20(2017).csv",
        "https://ourworldindata.org/grapher/cereal-yield.csv",
    ]
    for url in urls_to_try:
        try:
            resp = requests.get(url, timeout=30)
            if resp.status_code == 200:
                df = pd.read_csv(io.StringIO(resp.text))
                print(f"    Downloaded CSV with columns: {list(df.columns[:10])}")
                # Try to parse
                break
        except Exception as e:
            print(f"    Failed: {e}")

# 3. Merge on iso + year
if proxy_df is not None and len(proxy_df) > 0:
    print("\n[3] Merging target and proxy data...")
    # Filter target to overlapping years
    merged = target.merge(proxy_df[["iso", "year", "proxy_value"]], on=["iso", "year"])
    print(f"    Merged rows: {len(merged)}, countries: {merged['iso'].nunique()}")
    
    if len(merged) < 20:
        print("    WARNING: Fewer than 20 observations after merge — insufficient data")
        verdict = "inconclusive"
        result = build_result_json(
            "OEB-H08",
            "inconclusive",
            None, None,
            functional_form=None,
            data_quality_notes=(
                f"Proxy: {proxy_indicator_used}. Insufficient overlapping observations "
                f"({len(merged)}) after merging crop yield data with OEB target. "
                "Crop yield data coverage may not align well with OEB temporal range."
            ),
            summary="Insufficient data overlap between crop yield proxy and OEB target indicator.",
            verification_method="statistical_test"
        )
    else:
        print(f"    Proceeding with {len(merged)} observations from {merged['iso'].nunique()} countries")
        
        # 4. Bivariate correlation
        print("\n[4] Running bivariate correlation...")
        corr = run_bivariate_correlation(
            merged["proxy_value"], merged["value"], iso=merged["iso"]
        )
        print(f"    Pearson r={corr.pearson_r:.4f}, p={corr.pearson_p:.4f}")
        print(f"    Spearman rho={corr.spearman_rho:.4f}, p={corr.spearman_p:.4f}")
        print(f"    n_obs={corr.n_observations}, n_countries={corr.n_countries}")
        
        # 5. Partial correlation controlling for log(GDP per capita)
        print("\n[5] Running partial correlation controlling for log(GPC)...")
        gpc = load_raw_indicator("GPC")
        merged_gpc = merged.merge(
            gpc[["iso", "year", "value"]].rename(columns={"value": "gpc"}),
            on=["iso", "year"]
        )
        merged_gpc = merged_gpc.dropna(subset=["gpc"])
        merged_gpc["log_gpc"] = np.log(merged_gpc["gpc"].clip(lower=1e-6))
        print(f"    Rows for partial correlation: {len(merged_gpc)}")
        
        partial = None
        if len(merged_gpc) >= 20:
            partial = run_partial_correlation(
                merged_gpc, "proxy_value", "value", ["log_gpc"]
            )
            print(f"    Partial r={partial.partial_r:.4f}, p={partial.partial_p:.4f}")
        else:
            print("    Insufficient data for partial correlation")
        
        # 6. Functional form test
        print("\n[6] Testing functional form...")
        form = test_functional_form(merged["proxy_value"], merged["value"])
        print(f"    Best form: {form.best_form.value}")
        print(f"    Linear R²={form.linear_r2:.4f}, Log-linear R²={form.log_linear_r2:.4f}, Quadratic R²={form.quadratic_r2:.4f}")
        
        # 7. Verdict
        print("\n[7] Determining verdict...")
        verdict = determine_verdict(corr, partial, "negative")
        print(f"    Verdict: {verdict}")
        
        result = build_result_json(
            "OEB-H08",
            verdict,
            corr,
            partial,
            functional_form=form,
            data_quality_notes=(
                f"Proxy used: {proxy_indicator_used}. "
                "Crop yield (kg/ha) used as a downstream indicator of ozone damage — "
                "higher yields expected in areas with lower ozone stress (negative expected direction). "
                "Note: crop yields are influenced by many factors beyond ozone (fertilizers, irrigation, "
                "breeding improvements, weather), which may weaken the ozone signal. "
                "Yield data is national average, not KBA-specific. "
                "Secular trends in yield improvement may confound the analysis."
            ),
            summary=(
                f"Testing whether national crop yields (as proxy for integrated ozone damage) "
                f"are negatively correlated with OEB ozone exposure. "
                f"Pearson r={corr.pearson_r:.3f} (p={corr.pearson_p:.3f}), "
                f"Spearman rho={corr.spearman_rho:.3f} (p={corr.spearman_p:.3f}), "
                f"n={corr.n_observations} obs from {corr.n_countries} countries. "
                + (f"Partial r={partial.partial_r:.3f} (p={partial.partial_p:.3f}) controlling for log(GPC). " if partial else "Partial correlation not computed. ")
                + f"Best functional form: {form.best_form.value}. Verdict: {verdict}."
            ),
            verification_method="statistical_test"
        )

else:
    print("\n    All data acquisition attempts failed.")
    result = build_result_json(
        "OEB-H08",
        "inconclusive",
        None, None,
        functional_form=None,
        data_quality_notes=(
            "Failed to acquire crop yield proxy data. Attempted: "
            "(1) World Bank AG.YLD.CREL.KG (cereal yield), "
            "(2) World Bank AG.YLD.WHEA.KG (wheat yield), "
            "(3) Our World in Data CSV download. "
            "All sources were unavailable or returned insufficient data."
        ),
        summary="Proxy data acquisition failed for crop yield indicator from FAO/World Bank.",
        verification_method="statistical_test"
    )

# 8. Write result
result["verification_method"] = "statistical_test"
output_file = f"{output_path}/result.json"
with open(output_file, "w") as f:
    json.dump(result, f, indent=2)

print(f"\n[8] Results written to {output_file}")
print(f"    Final verdict: {result.get('verdict', 'unknown')}")
print("=== Done ===")