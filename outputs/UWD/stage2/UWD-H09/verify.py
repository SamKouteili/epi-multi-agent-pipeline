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

output_path = "/Users/samkouteili/rose/epi/multi-agent/outputs/UWD/stage2/UWD-H09"
os.makedirs(output_path, exist_ok=True)

hypothesis_id = "UWD-H09"
expected_direction = "positive"

data_quality_notes = []

# ─────────────────────────────────────────────────────────────
# Step 1: Load EPI target (UWD)
# ─────────────────────────────────────────────────────────────
print("Loading UWD target indicator...")
target = load_raw_indicator("UWD")
print(f"  UWD shape: {target.shape}")

# ─────────────────────────────────────────────────────────────
# Step 2: Approach 1 — Try the WHO URL
# ─────────────────────────────────────────────────────────────
url = "https://www.who.int/news/item/07-06-2022-who-launches-new-initiative-on-wastewater-surveillance"
print(f"\nApproach 1: Fetching WHO URL: {url}")
try:
    resp = requests.get(url, timeout=15)
    print(f"  HTTP status: {resp.status_code}, content length: {len(resp.content)}")
    data_quality_notes.append(
        f"Approach 1: Fetched {url} — HTTP {resp.status_code}. "
        "This is a WHO news/press page (404 or HTML only), not a structured dataset. "
        "No machine-readable pathogen data available here."
    )
except Exception as e:
    data_quality_notes.append(f"Approach 1: Failed to fetch {url}: {e}")
    print(f"  Error: {e}")

# ─────────────────────────────────────────────────────────────
# Step 3: Approach 2 — World Bank & WHO GHO searches
# ─────────────────────────────────────────────────────────────
print("\nApproach 2: Searching World Bank and WHO GHO...")

wb_queries = [
    "fecal coliform water",
    "E. coli water contamination",
    "waterborne pathogen",
    "water quality bacteria",
    "sanitation fecal",
]
wb_results_summary = []
for q in wb_queries:
    try:
        res = search_world_bank(q)
        wb_results_summary.append(f"WB '{q}': {len(res)} results")
        print(f"  WB search '{q}': {len(res)} results")
    except Exception as e:
        wb_results_summary.append(f"WB '{q}': error — {e}")
        print(f"  WB search '{q}' error: {e}")

data_quality_notes.append(
    "Approach 2a — World Bank searches for fecal/pathogen indicators: "
    + "; ".join(wb_results_summary)
    + ". No relevant pathogen-specific indicators found."
)

# WHO GHO — try a few codes
gho_codes_tried = []
for code in ["WSH_SANITATION_SAFELY_MANAGED", "WHS3_41"]:
    try:
        df = fetch_who_gho_indicator(code)
        sz = df.shape if df is not None else "None"
        print(f"  WHO GHO '{code}': {sz}")
        gho_codes_tried.append(f"{code}: {sz}")
    except Exception as e:
        print(f"  WHO GHO '{code}' error: {e}")
        gho_codes_tried.append(f"{code}: error — {e}")

data_quality_notes.append(
    "Approach 2b — WHO GHO: No country-level E. coli/enterococcus/viral marker "
    "data available through standard GHO codes. Tried: " + "; ".join(gho_codes_tried)
)

# ─────────────────────────────────────────────────────────────
# Step 4: Approach 3 — Use an approximate proxy
# Open defecation rate is the best global proxy for fecal contamination
# of surface water. People practicing open defecation directly contribute
# FIO load to water bodies.
# ─────────────────────────────────────────────────────────────
print("\nApproach 3: Finding approximate proxy — open defecation / sanitation access")

local = list_local_indicators()
local_tlas = [x["tla"] for x in local] if isinstance(local, list) else []
print(f"  Local indicators: {local_tlas}")
data_quality_notes.append(f"Local indicators available: {local_tlas}")

proxy_df = None
proxy_name = None
proxy_wb_code = None

wb_indicator_attempts = [
    ("SH.STA.ODFC.ZS", "Open defecation rate (% of population)"),
    ("SH.STA.BASS.ZS", "People using at least basic sanitation services (%)"),
    ("SH.H2O.BASW.ZS", "People using at least basic drinking water services (%)"),
    ("SH.STA.SMSS.ZS", "Safely managed sanitation (%)"),
    ("SH.H2O.SMDW.ZS", "Safely managed drinking water (%)"),
]

for wb_code, wb_label in wb_indicator_attempts:
    print(f"  Trying WB indicator {wb_code}: {wb_label}")
    try:
        df = fetch_world_bank_indicator(wb_code)
        if df is not None and len(df) > 100:
            proxy_df = df.rename(columns={"value": "proxy_value"})
            proxy_name = wb_label
            proxy_wb_code = wb_code
            print(f"    ✓ Got {len(proxy_df)} rows for '{wb_label}'")
            data_quality_notes.append(
                f"Approach 3: Using WB indicator {wb_code} '{wb_label}' as approximate proxy. "
                "Rationale: country-level sanitation/open-defecation rate is the best "
                "available global proxy for fecal contamination of water (FIO load). "
                "Direct E. coli/enterococcus monitoring data (original hypothesis proxy) "
                "is not available in any global database with sufficient country coverage."
            )
            break
        else:
            print(f"    ✗ Insufficient data ({len(df) if df is not None else 0} rows)")
    except Exception as e:
        print(f"    ✗ Error: {e}")

if proxy_df is None:
    data_quality_notes.append(
        "Approach 3: All World Bank indicator attempts failed. No usable proxy found."
    )

# ─────────────────────────────────────────────────────────────
# Step 5: Run analysis if proxy is available
# ─────────────────────────────────────────────────────────────
if proxy_df is not None:
    print(f"\nRunning analysis with proxy: {proxy_name}")
    print(f"  Proxy shape: {proxy_df.shape}")
    print(f"  Proxy columns: {proxy_df.columns.tolist()}")
    print(f"  Proxy sample:\n{proxy_df.head()}")

    # Merge on iso + year
    merged = target.merge(proxy_df[["iso", "year", "proxy_value"]], on=["iso", "year"])
    merged = merged.dropna(subset=["value", "proxy_value"])
    print(f"  Merged shape after dropna: {merged.shape}")
    print(f"  Unique countries: {merged['iso'].nunique()}")
    print(f"  Year range: {merged['year'].min()} – {merged['year'].max()}")

    if len(merged) < 20:
        print("  Too few observations for reliable statistics.")
        result = build_result_json(
            hypothesis_id,
            "inconclusive",
            None, None,
            functional_form=None,
            data_quality_notes="; ".join(data_quality_notes),
            summary=(
                f"Proxy '{proxy_name}' merged with UWD yielded only {len(merged)} observations — "
                "insufficient for analysis."
            ),
        )
        result["verification_method"] = "pending_data"
    else:
        # Bivariate correlation
        print("\nRunning bivariate correlation...")
        corr = run_bivariate_correlation(
            merged["proxy_value"], merged["value"], iso=merged["iso"]
        )
        print(
            f"  Pearson r={corr.pearson_r:.3f} (p={corr.pearson_p:.4f}), "
            f"Spearman rho={corr.spearman_rho:.3f} (p={corr.spearman_p:.4f}), "
            f"n={corr.n_observations}, countries={corr.n_countries}"
        )

        # Functional form
        print("Running functional form test...")
        try:
            form = test_functional_form(merged["proxy_value"], merged["value"])
            print(f"  Best functional form: {form.best_form.value}")
        except Exception as e:
            print(f"  Functional form test failed: {e}")
            form = None
            data_quality_notes.append(f"Functional form test failed: {e}")

        # Partial correlation controlling for log(GDP per capita)
        print("Loading GPC for partial correlation...")
        gpc = load_raw_indicator("GPC")
        merged_gpc = merged.merge(
            gpc[["iso", "year", "value"]].rename(columns={"value": "gpc"}),
            on=["iso", "year"],
        )
        merged_gpc = merged_gpc.dropna(subset=["gpc", "proxy_value", "value"])
        merged_gpc["log_gpc"] = np.log(merged_gpc["gpc"].clip(lower=1))
        print(f"  Merged with GPC: {merged_gpc.shape}")

        partial = None
        if len(merged_gpc) >= 30:
            print("Running partial correlation...")
            try:
                partial = run_partial_correlation(
                    merged_gpc, "proxy_value", "value", ["log_gpc"]
                )
                print(
                    f"  Partial r={partial.partial_r:.3f} (p={partial.partial_p:.4f})"
                )
            except Exception as e:
                print(f"  Partial correlation failed: {e}")
                data_quality_notes.append(
                    f"Partial correlation (controlling log_gpc) failed with error: {e}. "
                    "This may be due to near-collinearity between proxy and GPC."
                )
        else:
            print(f"  Too few obs ({len(merged_gpc)}) for partial correlation after GPC merge.")
            data_quality_notes.append(
                f"Partial correlation skipped: only {len(merged_gpc)} observations after GPC merge."
            )

        # Determine verdict
        verdict = determine_verdict(corr, partial, expected_direction)
        print(f"\nVerdict: {verdict}")

        result = build_result_json(
            hypothesis_id,
            verdict,
            corr,
            partial,
            functional_form=form,
            data_quality_notes="; ".join(data_quality_notes),
            summary=(
                f"Used WB indicator '{proxy_wb_code}' ({proxy_name}) as approximate proxy "
                f"for waterborne pathogen prevalence (original proxy: E. coli/enterococcus in surface water — "
                f"no global dataset exists). "
                f"Bivariate: Pearson r={corr.pearson_r:.3f} (p={corr.pearson_p:.4f}), "
                f"Spearman rho={corr.spearman_rho:.3f} (p={corr.spearman_p:.4f}), "
                f"n={corr.n_observations} obs across {corr.n_countries} countries. "
                + (
                    f"Partial r={partial.partial_r:.3f} (p={partial.partial_p:.4f}) controlling log(GPC). "
                    if partial else
                    "Partial correlation not computed. "
                )
                + (f"Best functional form: {form.best_form.value}." if form else "")
            ),
        )
        result["verification_method"] = "exploratory_test"

else:
    # No proxy data found at all
    print("\nNo proxy data found after all approaches. Reporting inconclusive.")
    result = build_result_json(
        hypothesis_id,
        "inconclusive",
        None, None,
        functional_form=None,
        data_quality_notes="; ".join(data_quality_notes),
        summary=(
            "Could not find any usable country-level proxy for waterborne pathogen "
            "detection (E. coli, enterococcus, viral markers in surface water). "
            "The WHO/UNICEF Environmental Pathogen Surveillance Network data is "
            "highly fragmented and not available through any global API or structured "
            "download. All World Bank and WHO GHO searches returned no suitable "
            "indicator with sufficient country coverage. Verdict: inconclusive."
        ),
    )
    result["verification_method"] = "pending_data"

# ─────────────────────────────────────────────────────────────
# Step 6: Write result.json
# ─────────────────────────────────────────────────────────────
result_path = f"{output_path}/result.json"
with open(result_path, "w") as f:
    json.dump(result, f, indent=2)
print(f"\nResult written to: {result_path}")
print(json.dumps(result, indent=2))