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
from src.utils.data_fetch import fetch_world_bank_indicator, search_world_bank

OUTPUT_DIR = "/Users/samkouteili/rose/epi/multi-agent/outputs/OEB/stage2/OEB-H10/"
os.makedirs(OUTPUT_DIR, exist_ok=True)

HYPOTHESIS_ID = "OEB-H10"
EXPECTED_DIRECTION = "positive"

print("=== OEB-H10: Ammonia Emissions / Livestock Density vs OEB ===")

# 1. Load EPI target data
print("\n[1] Loading OEB target indicator...")
target = load_raw_indicator("OEB")
print(f"    OEB shape: {target.shape}")
print(f"    Years: {sorted(target['year'].unique())}")
print(f"    Countries: {target['iso'].nunique()}")

# 2. Acquire proxy data
# Since EDGAR (already used by OEB-H04) and FAOSTAT (used by OEB-H08) are excluded,
# we'll try World Bank indicators for livestock density / agricultural ammonia proxies.
# Options:
#   - AG.LND.LVST.K2  : Livestock density (animals per sq km of agricultural land)
#   - EN.ATM.METH.AG.KT.CE : Agricultural methane (related but not ammonia)
#   - AG.PRD.LVSK.XD  : Livestock production index
#   - SL.AGR.EMPL.ZS  : Employment in agriculture (rough proxy)
# We'll try livestock density first, then fall back.

print("\n[2] Fetching proxy data...")

proxy = None
proxy_name = None

# Try livestock density
print("    Trying AG.LND.LVST.K2 (livestock density)...")
try:
    proxy = fetch_world_bank_indicator("AG.LND.LVST.K2")
    if proxy is not None and len(proxy) > 100:
        proxy_name = "Livestock density (animals per sq km of agricultural land)"
        print(f"    SUCCESS: {len(proxy)} rows, {proxy['iso'].nunique()} countries")
    else:
        print("    Insufficient data, trying alternative...")
        proxy = None
except Exception as e:
    print(f"    Failed: {e}")
    proxy = None

# Try livestock production index
if proxy is None:
    print("    Trying AG.PRD.LVSK.XD (livestock production index)...")
    try:
        proxy = fetch_world_bank_indicator("AG.PRD.LVSK.XD")
        if proxy is not None and len(proxy) > 100:
            proxy_name = "Livestock production index"
            print(f"    SUCCESS: {len(proxy)} rows, {proxy['iso'].nunique()} countries")
        else:
            proxy = None
    except Exception as e:
        print(f"    Failed: {e}")
        proxy = None

# Try agricultural methane (linked to livestock - cattle enteric fermentation & manure)
if proxy is None:
    print("    Trying EN.ATM.METH.AG.KT.CE (agricultural methane emissions)...")
    try:
        proxy = fetch_world_bank_indicator("EN.ATM.METH.AG.KT.CE")
        if proxy is not None and len(proxy) > 100:
            proxy_name = "Agricultural methane emissions (kt of CO2 equiv)"
            print(f"    SUCCESS: {len(proxy)} rows, {proxy['iso'].nunique()} countries")
        else:
            proxy = None
    except Exception as e:
        print(f"    Failed: {e}")
        proxy = None

# Try agricultural nitrous oxide (closer to ammonia/nitrogen cycle)
if proxy is None:
    print("    Trying EN.ATM.NOXE.AG.KT.CE (agricultural N2O emissions)...")
    try:
        proxy = fetch_world_bank_indicator("EN.ATM.NOXE.AG.KT.CE")
        if proxy is not None and len(proxy) > 100:
            proxy_name = "Agricultural nitrous oxide emissions (kt of CO2 equiv)"
            print(f"    SUCCESS: {len(proxy)} rows, {proxy['iso'].nunique()} countries")
        else:
            proxy = None
    except Exception as e:
        print(f"    Failed: {e}")
        proxy = None

# Try searching for ammonia-related indicators
if proxy is None:
    print("    Searching World Bank for ammonia-related indicators...")
    try:
        results = search_world_bank("ammonia agriculture livestock")
        print(f"    Search results: {results}")
    except Exception as e:
        print(f"    Search failed: {e}")

# Try arable land as agricultural activity proxy
if proxy is None:
    print("    Trying AG.LND.ARBL.ZS (arable land % of land area)...")
    try:
        proxy = fetch_world_bank_indicator("AG.LND.ARBL.ZS")
        if proxy is not None and len(proxy) > 100:
            proxy_name = "Arable land (% of land area)"
            print(f"    SUCCESS: {len(proxy)} rows, {proxy['iso'].nunique()} countries")
        else:
            proxy = None
    except Exception as e:
        print(f"    Failed: {e}")
        proxy = None

# If all World Bank attempts fail, write inconclusive
if proxy is None:
    print("\n[!] All proxy data acquisition attempts failed.")
    result = {
        "hypothesis_id": HYPOTHESIS_ID,
        "verdict": "inconclusive",
        "verification_method": "statistical_test",
        "data_quality_notes": (
            "Could not acquire proxy data for ammonia emissions or livestock density. "
            "EDGAR (primary source) was already used by OEB-H04 and is excluded. "
            "FAOSTAT was already used by OEB-H08 and is excluded. "
            "Attempted World Bank indicators: AG.LND.LVST.K2 (livestock density), "
            "AG.PRD.LVSK.XD (livestock production index), EN.ATM.METH.AG.KT.CE "
            "(agricultural methane), EN.ATM.NOXE.AG.KT.CE (agricultural N2O), "
            "AG.LND.ARBL.ZS (arable land). None returned sufficient data."
        ),
        "summary": (
            "Unable to verify hypothesis OEB-H10 due to unavailability of non-duplicate "
            "proxy data for ammonia emissions and livestock density."
        ),
    }
    out_path = os.path.join(OUTPUT_DIR, "result.json")
    with open(out_path, "w") as f:
        json.dump(result, f, indent=2)
    print(f"\nWritten inconclusive result to {out_path}")
    exit(0)

# 3. Prepare and merge
print("\n[3] Preparing proxy data...")
proxy = proxy.rename(columns={"value": "proxy_value"})
proxy = proxy[["iso", "year", "proxy_value"]].dropna(subset=["proxy_value"])
print(f"    Proxy after dropna: {len(proxy)} rows, {proxy['iso'].nunique()} countries")
print(f"    Proxy years: {sorted(proxy['year'].unique())}")

print("\n[4] Merging OEB target with proxy...")
merged = target.merge(proxy, on=["iso", "year"])
print(f"    Merged shape: {merged.shape}")
print(f"    Countries in merged: {merged['iso'].nunique()}")
print(f"    Years in merged: {sorted(merged['year'].unique())}")

if len(merged) < 20:
    print(f"\n[!] Insufficient merged data ({len(merged)} rows). Writing inconclusive.")
    result = {
        "hypothesis_id": HYPOTHESIS_ID,
        "verdict": "inconclusive",
        "verification_method": "statistical_test",
        "data_quality_notes": (
            f"Proxy used: {proxy_name}. "
            f"Only {len(merged)} matched observations after merging OEB target with proxy. "
            "Insufficient data for reliable correlation analysis (threshold: n >= 20)."
        ),
        "summary": "Inconclusive due to insufficient overlapping data.",
    }
    out_path = os.path.join(OUTPUT_DIR, "result.json")
    with open(out_path, "w") as f:
        json.dump(result, f, indent=2)
    print(f"Written inconclusive result to {out_path}")
    exit(0)

# 4. Bivariate correlation
print("\n[5] Running bivariate correlation...")
corr = run_bivariate_correlation(merged["proxy_value"], merged["value"], iso=merged["iso"])
print(f"    Pearson r={corr.pearson_r:.4f}, p={corr.pearson_p:.4f}")
print(f"    Spearman rho={corr.spearman_rho:.4f}, p={corr.spearman_p:.4f}")
print(f"    n_observations={corr.n_observations}, n_countries={corr.n_countries}")

# 5. Partial correlation controlling for log(GDP per capita)
print("\n[6] Running partial correlation (controlling for log GPC)...")
gpc = load_raw_indicator("GPC")
merged_gpc = merged.merge(
    gpc[["iso", "year", "value"]].rename(columns={"value": "gpc"}),
    on=["iso", "year"],
)
merged_gpc = merged_gpc.dropna(subset=["gpc"])
merged_gpc["log_gpc"] = np.log(merged_gpc["gpc"].replace(0, np.nan))
merged_gpc = merged_gpc.dropna(subset=["log_gpc"])
print(f"    Merged with GPC: {len(merged_gpc)} rows")

partial = None
if len(merged_gpc) >= 20:
    partial = run_partial_correlation(merged_gpc, "proxy_value", "value", ["log_gpc"])
    print(f"    Partial r={partial.partial_r:.4f}, p={partial.partial_p:.4f}")
else:
    print("    Insufficient data for partial correlation.")

# 6. Functional form test
print("\n[7] Testing functional forms...")
form = test_functional_form(merged["proxy_value"], merged["value"])
print(f"    Best form: {form.best_form.value}")
print(f"    Linear R²={form.linear_r2:.4f}, AIC={form.linear_aic:.2f}")
print(f"    Log-linear R²={form.log_linear_r2:.4f}, AIC={form.log_linear_aic:.2f}")
print(f"    Quadratic R²={form.quadratic_r2:.4f}, AIC={form.quadratic_aic:.2f}")

# 7. Verdict
print("\n[8] Determining verdict...")
verdict = determine_verdict(corr, partial, EXPECTED_DIRECTION)
print(f"    Verdict: {verdict.value}")

# 8. Build and write result
data_quality_notes = (
    f"Proxy used: {proxy_name} (World Bank). "
    "Primary proxy (EDGAR ammonia emissions) was excluded as already used by OEB-H04. "
    "FAOSTAT also excluded (used by OEB-H08). "
    f"Merged dataset: {corr.n_observations} observations across {corr.n_countries} countries. "
    "Livestock-related indicators are available primarily for years with World Bank coverage."
)

summary = (
    f"Testing whether {proxy_name} correlates positively with OEB (ozone exposure in KBAs). "
    f"Pearson r={corr.pearson_r:.3f} (p={corr.pearson_p:.3f}), "
    f"Spearman rho={corr.spearman_rho:.3f} (p={corr.spearman_p:.3f}). "
    + (f"Partial r={partial.partial_r:.3f} (p={partial.partial_p:.3f}) controlling for log(GPC). " if partial else "Partial correlation not computed. ")
    + f"Best functional form: {form.best_form.value}. "
    f"Verdict: {verdict.value}."
)

result = build_result_json(
    HYPOTHESIS_ID,
    verdict,
    corr,
    partial,
    functional_form=form,
    data_quality_notes=data_quality_notes,
    summary=summary,
)
result["verification_method"] = "statistical_test"

out_path = os.path.join(OUTPUT_DIR, "result.json")
with open(out_path, "w") as f:
    json.dump(result, f, indent=2)

print(f"\n=== Done. Result written to {out_path} ===")
print(json.dumps(result, indent=2))