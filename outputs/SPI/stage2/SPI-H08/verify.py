import json
import os
import requests
import pandas as pd
import numpy as np

from src.utils.stats import run_bivariate_correlation, run_partial_correlation, determine_verdict, build_result_json, test_functional_form
from src.utils.data_utils import load_raw_indicator
from src.utils.data_fetch import fetch_world_bank_indicator, search_world_bank, list_local_indicators

output_path = "/Users/samkouteili/rose/epi/multi-agent/outputs/SPI/stage2/SPI-H08"
os.makedirs(output_path, exist_ok=True)

print("=== SPI-H08: Area of Habitat Remaining within Fragmented Landscape Patches ===")
print()

# 1. Load EPI target data
print("Loading SPI target data...")
target = load_raw_indicator("SPI")
print(f"  SPI data: {len(target)} rows, {target['iso'].nunique()} countries")

# 2. Approach 1: Try the direct URL (WRI forest loss insights page - likely HTML/article, not data)
print("\nApproach 1: Trying direct URL fetch from WRI...")
try:
    resp = requests.get("https://www.wri.org/insights/forest-loss-drivers-data-trends", timeout=15)
    print(f"  URL status: {resp.status_code} — likely an article page, not raw data")
except Exception as e:
    print(f"  URL fetch failed: {e}")

# 3. Approach 2: Check local indicators
print("\nApproach 2: Checking local indicators...")
local = list_local_indicators()
local_tlas = [x['tla'] for x in local] if local else []
print(f"  Local indicator TLAs: {local_tlas}")

# 4. Approach 3: Search World Bank for related indicators
print("\nApproach 3: Searching World Bank for related indicators...")
search_queries = [
    "forest fragmentation habitat",
    "forest area remaining",
    "primary forest area",
    "tree cover loss",
    "forest landscape integrity"
]

for q in search_queries:
    try:
        results = search_world_bank(q)
        if results is not None and len(results) > 0:
            print(f"  Query '{q}': {len(results)} results")
            print(f"    Top results:\n{results[['id','name']].head(3).to_string()}")
    except Exception as e:
        print(f"  Query '{q}' failed: {e}")

# 5. Try specific World Bank indicators related to forest area
print("\nApproach 3b: Fetching specific WB indicators related to forest/habitat...")

proxy_candidates = [
    ("AG.LND.FRST.ZS", "Forest area (% of land area)"),
    ("AG.LND.FRST.K2", "Forest area (sq. km)"),
]

proxy_data = None
proxy_name = None
proxy_wb_code = None
proxy_col = "proxy_value"

for code, name in proxy_candidates:
    print(f"\n  Trying WB indicator: {code} ({name})")
    try:
        df = fetch_world_bank_indicator(code)
        if df is not None and len(df) > 0:
            df = df.rename(columns={"value": proxy_col})
            df = df.dropna(subset=[proxy_col])
            print(f"    Got {len(df)} rows, {df['iso'].nunique()} countries")
            merged_test = target.merge(df, on=["iso", "year"])
            merged_test = merged_test.dropna(subset=[proxy_col, "value"])
            print(f"    Overlap with SPI: {len(merged_test)} rows, {merged_test['iso'].nunique()} countries")
            if len(merged_test) >= 20 and proxy_data is None:
                proxy_data = df
                proxy_name = name
                proxy_wb_code = code
                print(f"    -> Selected as proxy!")
    except Exception as e:
        print(f"    Failed: {e}")

# 6. Run analysis or report failure
if proxy_data is None:
    print("\nAll approaches failed — no usable proxy data found.")
    result = {
        "hypothesis_id": "SPI-H08",
        "target_indicator": "SPI",
        "proxy_variable": "Area of Habitat Remaining within Fragmented Landscape Patches",
        "verification_method": "pending_data",
        "verdict": "inconclusive",
        "data_quality_notes": (
            "Could not obtain exact proxy data for habitat fragmentation metrics. "
            "Approach 1: WRI URL (https://www.wri.org/insights/forest-loss-drivers-data-trends) is an article page, not raw data. "
            "Approach 2: No relevant local indicators found for habitat fragmentation. "
            "Approach 3: World Bank searches for forest fragmentation keywords did not return usable tabular data. "
            "Approach 3b: Failed to fetch World Bank indicator data programmatically. "
            "The exact proxy requires geospatial raster processing (Global Forest Watch / ESA CCI Land Cover) not available via standard APIs."
        ),
        "summary": "No usable proxy data could be obtained for habitat fragmentation. The hypothesis requires geospatial raster processing of Global Forest Watch or ESA CCI data, which is not available via standard data APIs."
    }
    out_file = f"{output_path}/result.json"
    with open(out_file, "w") as f:
        json.dump(result, f, indent=2)
    print(f"\nResult written to {out_file}")

else:
    print(f"\n=== Running analysis with proxy: {proxy_name} ===")

    # Merge
    merged = target.merge(proxy_data, on=["iso", "year"])
    merged = merged.dropna(subset=["proxy_value", "value"])
    print(f"Merged dataset: {len(merged)} rows, {merged['iso'].nunique()} countries")

    # Bivariate correlation
    print("\nRunning bivariate correlation...")
    corr = run_bivariate_correlation(merged["proxy_value"], merged["value"], iso=merged["iso"])
    print(f"  Pearson r={corr.pearson_r:.4f}, p={corr.pearson_p:.4f}")
    print(f"  Spearman rho={corr.spearman_rho:.4f}, p={corr.spearman_p:.4f}")
    print(f"  n_observations={corr.n_observations}, n_countries={corr.n_countries}")

    # Partial correlation controlling for log(GDP per capita)
    print("\nRunning partial correlation controlling for log(GPC)...")
    gpc = load_raw_indicator("GPC")
    merged_gpc = merged.merge(
        gpc[["iso", "year", "value"]].rename(columns={"value": "gpc"}),
        on=["iso", "year"]
    )
    merged_gpc = merged_gpc.dropna(subset=["gpc"])
    merged_gpc["log_gpc"] = np.log(merged_gpc["gpc"].clip(lower=1))
    print(f"  Partial correlation dataset: {len(merged_gpc)} rows")

    partial = run_partial_correlation(merged_gpc, "proxy_value", "value", ["log_gpc"])
    print(f"  Partial r={partial.partial_r:.4f}, p={partial.partial_p:.4f}")

    # Functional form test
    print("\nTesting functional form...")
    form = test_functional_form(merged["proxy_value"], merged["value"])
    print(f"  Best form: {form.best_form.value}")
    # Safely print R2 values (may be None)
    linear_r2_str = f"{form.linear_r2:.4f}" if form.linear_r2 is not None else "None"
    log_r2_str = f"{form.log_linear_r2:.4f}" if form.log_linear_r2 is not None else "None"
    quad_r2_str = f"{form.quadratic_r2:.4f}" if form.quadratic_r2 is not None else "None"
    print(f"  Linear R2={linear_r2_str}, Log-linear R2={log_r2_str}, Quadratic R2={quad_r2_str}")

    # Verdict
    verdict = determine_verdict(corr, partial, "positive")
    print(f"\nVerdict: {verdict.value}")

    data_quality_notes = (
        f"Exact proxy (area of habitat in patches > minimum viable size) unavailable via standard APIs — requires GIS raster processing. "
        f"Substituted with World Bank '{proxy_name}' (code: {proxy_wb_code}) as an approximate proxy for habitat availability. "
        f"Forest area % captures broad habitat availability but does NOT capture fragmentation specifically. "
        f"This is an exploratory test using an imperfect proxy. "
        f"Approach 1: WRI URL was an article page. "
        f"Approach 2: No local fragmentation indicators found. "
        f"Approach 3: World Bank searches did not yield fragmentation metrics; fell back to forest area %."
    )

    result = build_result_json(
        "SPI-H08",
        verdict,
        corr,
        partial,
        functional_form=form,
        data_quality_notes=data_quality_notes,
        summary=(
            f"Using '{proxy_name}' as approximate proxy for habitat availability (not fragmentation per se). "
            f"Bivariate: Pearson r={corr.pearson_r:.3f} (p={corr.pearson_p:.4f}), "
            f"Spearman rho={corr.spearman_rho:.3f}. "
            f"Partial r={partial.partial_r:.3f} (p={partial.partial_p:.4f}) controlling for log(GDP/capita). "
            f"Best functional form: {form.best_form.value}. "
            f"Verdict: {verdict.value}. "
            f"Note: proxy does not capture habitat fragmentation geometry; only broad forest area coverage."
        )
    )

    # Add verification_method and substitution notes
    result["verification_method"] = "exploratory_test"
    result["proxy_substitution"] = {
        "requested": "Area of Habitat Remaining within Fragmented Landscape Patches",
        "used": proxy_name,
        "wb_code": proxy_wb_code,
        "rationale": "Forest area % is the most accessible proxy for habitat availability; does not capture fragmentation geometry"
    }

    out_file = f"{output_path}/result.json"
    with open(out_file, "w") as f:
        json.dump(result, f, indent=2)
    print(f"\nResult written to {out_file}")

print("\nDone.")