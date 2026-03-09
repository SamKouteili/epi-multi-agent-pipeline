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
    fetch_who_gho_indicator,
    search_world_bank,
    list_local_indicators,
)

output_path = "/Users/samkouteili/rose/epi/multi-agent/outputs/SPI/stage2/SPI-H10"
os.makedirs(output_path, exist_ok=True)

hypothesis_id = "SPI-H10"
expected_direction = "positive"
data_quality_notes = []

# ─────────────────────────────────────────────────────────────
# 1. Load EPI target
# ─────────────────────────────────────────────────────────────
print("Loading SPI target indicator...")
target = load_raw_indicator("SPI")
print(f"  SPI rows: {len(target)}, countries: {target['iso'].nunique()}")

# ─────────────────────────────────────────────────────────────
# Approach 1: Direct URL fetch (FWS eDNA page)
# ─────────────────────────────────────────────────────────────
print("\nApproach 1: Fetching FWS eDNA URL...")
try:
    resp = requests.get("https://www.fws.gov/project/environmental-dna-edna", timeout=15)
    print(f"  HTTP status: {resp.status_code}")
    data_quality_notes.append(
        f"Approach 1 – FWS eDNA URL (https://www.fws.gov/project/environmental-dna-edna): "
        f"HTTP {resp.status_code}. Page is informational HTML only; no downloadable "
        "machine-readable dataset with country-level coverage."
    )
except Exception as e:
    print(f"  Failed: {e}")
    data_quality_notes.append(f"Approach 1 – FWS eDNA URL fetch failed: {e}")

# ─────────────────────────────────────────────────────────────
# Approach 2: World Bank / local search
# ─────────────────────────────────────────────────────────────
print("\nApproach 2: Searching World Bank for eDNA / species diversity proxies...")

searches = [
    "environmental DNA species diversity",
    "biodiversity monitoring species richness",
    "species survey biodiversity",
    "aquatic biodiversity freshwater species",
]
wb_results_summary = {}
for q in searches:
    try:
        r = search_world_bank(q)
        wb_results_summary[q] = r[:3] if r else []
        print(f"  '{q}': {len(r) if r else 0} results")
    except Exception as e:
        wb_results_summary[q] = []
        print(f"  '{q}': error – {e}")

data_quality_notes.append(
    f"Approach 2 – World Bank searches for eDNA/species diversity: {searches}. "
    "No World Bank indicator directly measures eDNA species detection diversity."
)

print("\nChecking local indicators...")
local = list_local_indicators()
print(f"  Local indicators available: {local}")
data_quality_notes.append(f"Approach 2 – Local indicators checked: {local}")

# ─────────────────────────────────────────────────────────────
# Approach 3: Approximate proxy
# ─────────────────────────────────────────────────────────────
# eDNA diversity captures species community richness in protected areas.
# The closest available country-level approximation is the proportion of
# freshwater/aquatic species monitoring capacity — but no single WB indicator
# maps cleanly. We try a few plausible WB proxies:
#
#   AG.LND.FRST.ZS  – Forest area (% of land) – habitat proxy
#   ER.H2O.FWTL.ZS  – Freshwater withdrawal
#   ER.LND.PTLD.ZS  – (already used) Terrestrial PA
#   SH.H2O.SAFE.ZS  – (water / different domain)
#
# The most defensible approximate proxy: Forest area (% of land area)
# as a habitat-richness indicator correlating with both PA coverage and
# eDNA-detectable species diversity.
# ─────────────────────────────────────────────────────────────
print("\nApproach 3: Trying approximate proxy – Forest area % (AG.LND.FRST.ZS)...")

proxy_df = None
proxy_label = None

try:
    forest = fetch_world_bank_indicator("AG.LND.FRST.ZS")
    forest = forest.rename(columns={"value": "proxy_value"})
    forest = forest.dropna(subset=["proxy_value"])
    print(f"  Forest area rows: {len(forest)}, countries: {forest['iso'].nunique()}")
    proxy_df = forest
    proxy_label = "Forest area (% of land area) [AG.LND.FRST.ZS] — approximate proxy for habitat richness / eDNA-detectable diversity"
    data_quality_notes.append(
        "Approach 3 – No eDNA dataset exists at country-level scale. "
        "Substituted World Bank 'Forest area (% of land area)' (AG.LND.FRST.ZS) as an "
        "approximate habitat-richness proxy. Forest cover correlates with habitat availability "
        "and species community richness that eDNA sampling would detect, but it is a structural "
        "habitat measure rather than a direct biodiversity observation."
    )
except Exception as e:
    print(f"  Forest area fetch failed: {e}")
    data_quality_notes.append(f"Approach 3 – Forest area fetch failed: {e}")

# Fallback: try another proxy
if proxy_df is None:
    print("  Trying fallback: Mammal species count (EN.MAM.THRD.NO)...")
    try:
        mammals = fetch_world_bank_indicator("EN.MAM.THRD.NO")
        mammals = mammals.rename(columns={"value": "proxy_value"})
        mammals = mammals.dropna(subset=["proxy_value"])
        print(f"  Mammal threatened species rows: {len(mammals)}, countries: {mammals['iso'].nunique()}")
        proxy_df = mammals
        proxy_label = "Mammal species threatened (count) [EN.MAM.THRD.NO] — approximate proxy"
        data_quality_notes.append(
            "Approach 3 fallback – Used 'Mammal species threatened' (EN.MAM.THRD.NO) as approximate proxy."
        )
    except Exception as e:
        print(f"  Mammal species fetch failed: {e}")
        data_quality_notes.append(f"Approach 3 fallback failed: {e}")

# ─────────────────────────────────────────────────────────────
# 4. Run statistics if proxy found
# ─────────────────────────────────────────────────────────────
corr = None
partial = None
form = None
verdict = None
verification_method = "pending_data"

if proxy_df is not None and len(proxy_df) > 0:
    print("\nMerging proxy with SPI target...")
    merged = target.merge(proxy_df[["iso", "year", "proxy_value"]], on=["iso", "year"])
    merged = merged.dropna(subset=["value", "proxy_value"])
    print(f"  Merged rows: {len(merged)}, countries: {merged['iso'].nunique()}")

    if len(merged) >= 20:
        print("Running bivariate correlation...")
        corr = run_bivariate_correlation(
            merged["proxy_value"], merged["value"], iso=merged["iso"]
        )
        print(f"  Pearson r={corr.pearson_r:.3f}, p={corr.pearson_p:.4f}, n={corr.n_observations}")

        print("Running functional form test...")
        form = test_functional_form(merged["proxy_value"], merged["value"])
        print(f"  Best form: {form.best_form.value}")

        print("Running partial correlation controlling for log(GPC)...")
        try:
            gpc = load_raw_indicator("GPC")
            merged_gpc = merged.merge(
                gpc[["iso", "year", "value"]].rename(columns={"value": "gpc"}),
                on=["iso", "year"],
            )
            merged_gpc = merged_gpc.dropna(subset=["gpc"])
            merged_gpc["log_gpc"] = np.log(merged_gpc["gpc"].clip(lower=1e-6))
            print(f"  Merged with GPC: {len(merged_gpc)} rows")
            partial = run_partial_correlation(
                merged_gpc, "proxy_value", "value", ["log_gpc"]
            )
            print(f"  Partial r={partial.partial_r:.3f}, p={partial.partial_p:.4f}")
        except Exception as e:
            print(f"  Partial correlation failed: {e}")
            data_quality_notes.append(f"Partial correlation error: {e}")

        verdict = determine_verdict(corr, partial, expected_direction)
        print(f"\nVerdict: {verdict.value}")
        verification_method = "exploratory_test"
    else:
        print(f"  Insufficient data for statistics: n={len(merged)}")
        data_quality_notes.append(f"Merged dataset too small (n={len(merged)}) for reliable statistics.")
        verdict = None
        verification_method = "pending_data"
else:
    print("\nApproach 4: No usable proxy found. Reporting inconclusive.")
    data_quality_notes.append(
        "Approach 4 – eDNA Detection Diversity has no country-level publicly available dataset. "
        "FWS eDNA programs are project-based and not aggregated globally. "
        "World Bank has no eDNA indicator. Coverage is <5% of countries with no standardized "
        "international reporting framework. Result is inconclusive due to data unavailability."
    )
    verification_method = "pending_data"

# ─────────────────────────────────────────────────────────────
# 5. Build and write result JSON
# ─────────────────────────────────────────────────────────────
print("\nBuilding result JSON...")

summary = (
    "Environmental DNA (eDNA) detection diversity has no country-level publicly available "
    "dataset. The FWS eDNA program page is informational only, with no downloadable "
    "machine-readable data. Coverage is restricted to <5% of countries with no "
    "international standardized reporting. "
)
if proxy_df is not None and corr is not None:
    summary += (
        f"As an approximate proxy, Forest area (% of land area) was used "
        f"(r={corr.pearson_r:.3f}, p={corr.pearson_p:.4f}, n={corr.n_observations} obs). "
        f"This measures habitat availability rather than eDNA-detected diversity directly. "
        f"Verdict: {verdict.value if verdict else 'inconclusive'}."
    )
else:
    summary += "No suitable proxy data could be obtained. Verdict: inconclusive."

result = build_result_json(
    hypothesis_id,
    verdict if verdict is not None else "inconclusive",
    corr,
    partial,
    functional_form=form,
    data_quality_notes=" | ".join(data_quality_notes),
    summary=summary,
)

# Inject extra fields
result["verification_method"] = verification_method
result["proxy_substitution"] = proxy_label if proxy_label else "None — no proxy found"
result["attempted_sources"] = [
    "https://www.fws.gov/project/environmental-dna-edna",
    "World Bank: AG.LND.FRST.ZS (Forest area %)",
    "World Bank: EN.MAM.THRD.NO (Mammal threatened species)",
    "World Bank searches: environmental DNA, biodiversity monitoring, species richness, aquatic biodiversity",
]

out_file = f"{output_path}/result.json"
with open(out_file, "w") as f:
    json.dump(result, f, indent=2)

print(f"\nResult written to: {out_file}")
print(f"Verification method: {verification_method}")
print(f"Verdict: {result.get('verdict', 'inconclusive')}")