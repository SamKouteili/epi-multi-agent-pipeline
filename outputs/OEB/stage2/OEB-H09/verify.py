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
from src.utils.data_fetch import fetch_world_bank_indicator, search_world_bank

output_path = "/Users/samkouteili/rose/epi/multi-agent/outputs/OEB/stage2/OEB-H09"
os.makedirs(output_path, exist_ok=True)

print("=== OEB-H09: Net Primary Productivity vs OEB ===")
print()

# 1. Load EPI target data
print("Loading OEB target indicator...")
target = load_raw_indicator("OEB")
print(f"  OEB data: {len(target)} rows, {target['iso'].nunique()} countries")

# 2. Acquire proxy data: Net Primary Productivity
# MODIS NPP is HDF4 format and not easily accessible via simple APIs.
# Use World Bank forest area (AG.LND.FRST.ZS) as proxy for NPP,
# since forest cover is the dominant component of terrestrial NPP.

print("\nTrying World Bank forest area as NPP proxy (AG.LND.FRST.ZS)...")
proxy = None
data_quality_notes = ""

try:
    forest = fetch_world_bank_indicator("AG.LND.FRST.ZS")
    if forest is not None and len(forest) > 100:
        forest = forest.rename(columns={"value": "proxy_value"})
        forest = forest[["iso", "year", "proxy_value"]].dropna()
        print(f"  Forest area data: {len(forest)} rows, {forest['iso'].nunique()} countries")
        proxy = forest
        data_quality_notes = (
            "MODIS NPP data is in HDF4 format and not accessible via standard APIs. "
            "Used World Bank AG.LND.FRST.ZS (Forest area % of land area) as proxy for "
            "Net Primary Productivity, as forest cover is a major component of terrestrial NPP. "
            "This is an imperfect substitute — forest area reflects standing biomass but not "
            "actual annual carbon flux. MODIS NPP uncertainty is ±20-30%; forest area has its own "
            "measurement issues. The negative direction (higher forest area → lower ozone exposure "
            "in KBAs) is plausible if forested regions have lower anthropogenic ozone sources."
        )
    else:
        print("  Forest area data insufficient.")
except Exception as e:
    print(f"  Forest area fetch failed: {e}")

# If forest area didn't work, try cereal yield as productivity proxy
if proxy is None:
    print("\nTrying cereal yield (AG.YLD.CREL.KG) as productivity proxy...")
    try:
        cereal = fetch_world_bank_indicator("AG.YLD.CREL.KG")
        if cereal is not None and len(cereal) > 100:
            cereal = cereal.rename(columns={"value": "proxy_value"})
            cereal = cereal[["iso", "year", "proxy_value"]].dropna()
            print(f"  Cereal yield data: {len(cereal)} rows, {cereal['iso'].nunique()} countries")
            proxy = cereal
            data_quality_notes = (
                "MODIS NPP (HDF4) not directly accessible via API. "
                "Used World Bank AG.YLD.CREL.KG (Cereal yield kg/ha) as proxy for productivity, "
                "reflecting agricultural NPP. This is a partial proxy for total NPP."
            )
    except Exception as e:
        print(f"  Cereal yield fetch failed: {e}")

# 3. Merge and analyze
if proxy is None or len(proxy) == 0:
    print("\nNo proxy data available. Writing inconclusive result.")
    result = {
        "hypothesis_id": "OEB-H09",
        "verdict": "inconclusive",
        "verification_method": "statistical_test",
        "data_quality_notes": (
            "MODIS NPP data is in HDF4 format and not accessible via standard APIs. "
            "World Bank alternative proxies (forest area, cereal yield) could not be retrieved. "
            "No suitable NPP proxy was available for statistical testing."
        ),
        "summary": "Could not acquire NPP proxy data for analysis.",
    }
    out_file = f"{output_path}/result.json"
    with open(out_file, "w") as f:
        json.dump(result, f, indent=2)
    print(f"Result written to {out_file}")
else:
    print(f"\nMerging proxy with OEB target data...")
    merged = target.merge(proxy, on=["iso", "year"])
    print(f"  Merged: {len(merged)} rows, {merged['iso'].nunique()} countries")

    if len(merged) < 20:
        print("  Insufficient data after merge. Writing inconclusive result.")
        result = {
            "hypothesis_id": "OEB-H09",
            "verdict": "inconclusive",
            "verification_method": "statistical_test",
            "data_quality_notes": data_quality_notes + " Insufficient overlap after merging.",
            "summary": "Insufficient data overlap between proxy and OEB target.",
        }
        out_file = f"{output_path}/result.json"
        with open(out_file, "w") as f:
            json.dump(result, f, indent=2)
        print(f"Result written to {out_file}")
    else:
        # 4. Bivariate correlation
        print("\nRunning bivariate correlation...")
        corr = run_bivariate_correlation(
            merged["proxy_value"], merged["value"], iso=merged["iso"]
        )
        print(f"  Pearson r={corr.pearson_r:.4f}, p={corr.pearson_p:.4e}")
        print(f"  Spearman rho={corr.spearman_rho:.4f}, p={corr.spearman_p:.4e}")
        print(f"  n={corr.n_observations}, n_countries={corr.n_countries}")

        # 5. Partial correlation controlling for log(GDP per capita)
        print("\nLoading GPC for partial correlation...")
        gpc = load_raw_indicator("GPC")
        merged_gpc = merged.merge(
            gpc[["iso", "year", "value"]].rename(columns={"value": "gpc"}),
            on=["iso", "year"],
        )
        merged_gpc = merged_gpc.dropna(subset=["gpc"])
        merged_gpc["log_gpc"] = np.log(merged_gpc["gpc"].clip(lower=1e-9))
        print(f"  Merged with GPC: {len(merged_gpc)} rows")

        partial = None
        if len(merged_gpc) >= 20:
            print("  Running partial correlation (controlling for log GPC)...")
            partial = run_partial_correlation(
                merged_gpc, "proxy_value", "value", ["log_gpc"]
            )
            print(f"  Partial r={partial.partial_r:.4f}, p={partial.partial_p:.4e}")
        else:
            print("  Insufficient data for partial correlation.")

        # 6. Functional form test
        print("\nTesting functional forms...")
        form = test_functional_form(merged["proxy_value"], merged["value"])
        print(f"  Best form: {form.best_form.value}")

        # Safely format potentially None values
        def fmt_r2(val):
            return f"{val:.4f}" if val is not None else "N/A"

        def fmt_aic(val):
            return f"{val:.2f}" if val is not None else "N/A"

        print(f"  Linear R²={fmt_r2(form.linear_r2)}, AIC={fmt_aic(form.linear_aic)}")
        print(f"  Log-linear R²={fmt_r2(form.log_linear_r2)}, AIC={fmt_aic(form.log_linear_aic)}")
        print(f"  Quadratic R²={fmt_r2(form.quadratic_r2)}, AIC={fmt_aic(form.quadratic_aic)}")

        # 7. Verdict
        print("\nDetermining verdict...")
        verdict = determine_verdict(corr, partial, "negative")
        print(f"  Verdict: {verdict.value}")

        partial_summary = ""
        if partial is not None:
            partial_summary = (
                f"Partial r={partial.partial_r:.3f} (p={partial.partial_p:.4e}) "
                f"controlling for log(GDP/capita)."
            )
        else:
            partial_summary = "Partial correlation not computed (insufficient data)."

        summary = (
            f"Testing World Bank forest area (% of land) as a proxy for MODIS NPP against OEB "
            f"(ozone exposure in Key Biodiversity Areas). "
            f"Pearson r={corr.pearson_r:.3f} (p={corr.pearson_p:.3e}), "
            f"Spearman rho={corr.spearman_rho:.3f}, "
            f"n={corr.n_observations} obs across {corr.n_countries} countries. "
            f"Best functional form: {form.best_form.value}. "
            f"{partial_summary}"
        )

        result = build_result_json(
            "OEB-H09",
            verdict,
            corr,
            partial,
            functional_form=form,
            data_quality_notes=data_quality_notes,
            summary=summary,
        )
        result["verification_method"] = "statistical_test"

        out_file = f"{output_path}/result.json"
        with open(out_file, "w") as f:
            json.dump(result, f, indent=2)
        print(f"\nResult written to {out_file}")
        print(f"Final verdict: {verdict.value}")