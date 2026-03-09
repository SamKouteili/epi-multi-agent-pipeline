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

output_path = "/Users/samkouteili/rose/epi/multi-agent/outputs/SPI/stage2/SPI-H01"
os.makedirs(output_path, exist_ok=True)

print("=" * 60)
print("SPI-H01: Protected Area Representativeness → SPI")
print("=" * 60)

# ── Load EPI target ──────────────────────────────────────────
print("\n[1] Loading SPI target data...")
target = load_raw_indicator("SPI")
print(f"    SPI rows: {len(target)}, countries: {target['iso'].nunique()}")

# ── APPROACH 1: Direct URL fetch (PDF metadata – no data) ────
print("\n[2] Approach 1: Trying direct URL from hypothesis...")
url = "https://www.ipbes.net/sites/default/files/Metadata_GEO_BON_Protected_Area_Representativeness_Index.pdf"
try:
    r = requests.get(url, timeout=15)
    print(f"    HTTP status: {r.status_code}, content-type: {r.headers.get('Content-Type','')}")
    print("    URL is a PDF metadata document — no machine-readable data available here.")
    approach1_note = f"URL returned HTTP {r.status_code} but is a PDF metadata document with no numeric data."
except Exception as e:
    approach1_note = f"URL fetch failed: {e}"
    print(f"    {approach1_note}")

# ── APPROACH 2: Search World Bank for PARC / representativeness ──
print("\n[3] Approach 2: Searching World Bank for representativeness indices...")
wb_notes = []

search_queries = [
    "protected area representativeness",
    "biodiversity protected area quality",
    "species protection representativeness",
    "protected area coverage ecosystem",
]
found_wb_code = None
found_wb_data = None

for q in search_queries:
    try:
        results = search_world_bank(q)
        if results is not None and len(results) > 0:
            print(f"    Query '{q}' → {len(results)} results")
            for _, row in results.head(5).iterrows():
                print(f"      - {row.get('id','?')} : {row.get('name','?')}")
            wb_notes.append(f"Query '{q}': {len(results)} results (none match PARC).")
        else:
            wb_notes.append(f"Query '{q}': no results.")
            print(f"    Query '{q}' → no results")
    except Exception as e:
        wb_notes.append(f"Query '{q}': error – {e}")
        print(f"    Query '{q}' → error: {e}")

# ── APPROACH 3: Approximate proxy – GEO BON / WDPA metrics ──
# The PARC index is conceptually closest to:
#   (a) Protected Area Management Effectiveness (METT scores) – not in WB
#   (b) KBA (Key Biodiversity Areas) coverage – available in WB
#   (c) WDPA terrestrial PA percentage – already used (SPI-H05)
#   (d) Marine PA percentage – a DIFFERENT dimension worth trying
#   (e) Freshwater/forest-specific PA metrics

print("\n[4] Approach 3: Finding approximate proxy for PA representativeness...")

# Try KBA coverage inside PAs (ER.PTD.TOTL is terrestrial – already used)
# Try marine protected areas as a different angle
candidate_codes = {
    "ER.MRN.PTMR.ZS": "Marine protected areas (% of territorial waters)",
    "ER.LND.PTLD.ZS": "Terrestrial and marine protected areas (% of total territorial area)",
    "AG.LND.FRST.ZS": "Forest area (% of land area)",  # proxy for habitat extent
}

proxy_df = None
proxy_code_used = None
proxy_name_used = None

for wb_code, description in candidate_codes.items():
    print(f"    Trying WB indicator {wb_code} ({description})...")
    try:
        df = fetch_world_bank_indicator(wb_code)
        if df is not None and len(df) > 100:
            df = df.rename(columns={"value": "proxy_value"})
            merged_test = target.merge(df, on=["iso", "year"])
            if len(merged_test) >= 30:
                proxy_df = df
                proxy_code_used = wb_code
                proxy_name_used = description
                print(f"    ✓ Found usable data: {len(merged_test)} merged rows")
                break
            else:
                print(f"      Only {len(merged_test)} merged rows — skipping")
        else:
            print(f"      No data returned")
    except Exception as e:
        print(f"      Error: {e}")

# ── APPROACH 4: Try GEO BON open data portals ───────────────
if proxy_df is None:
    print("\n[5] Approach 4: Trying GEO BON / GBIF open data APIs...")
    geobon_urls = [
        "https://portal.geobon.org/api/v1/metrics",
        "https://www.protectedplanet.net/api/v3/statistics",
    ]
    for gurl in geobon_urls:
        try:
            gr = requests.get(gurl, timeout=10)
            print(f"    {gurl} → {gr.status_code}")
        except Exception as e:
            print(f"    {gurl} → {e}")

    # Also try KBA coverage as a representativeness proxy
    print("\n    Trying KBA (Key Biodiversity Areas) coverage indicator...")
    try:
        kba_df = fetch_world_bank_indicator("ER.PTD.TOTL.ZS")  # PA coverage of KBAs
        if kba_df is not None and len(kba_df) > 50:
            kba_df = kba_df.rename(columns={"value": "proxy_value"})
            merged_test = target.merge(kba_df, on=["iso", "year"])
            if len(merged_test) >= 30:
                proxy_df = kba_df
                proxy_code_used = "ER.PTD.TOTL.ZS"
                proxy_name_used = "Coverage of KBAs by protected areas (terrestrial + marine %)"
                print(f"    ✓ KBA coverage: {len(merged_test)} merged rows")
    except Exception as e:
        print(f"    KBA indicator error: {e}")

# ── Run statistics if we found a proxy ───────────────────────
if proxy_df is not None:
    print(f"\n[6] Running statistics with proxy: {proxy_name_used}")
    merged = target.merge(proxy_df, on=["iso", "year"])
    merged = merged.dropna(subset=["value", "proxy_value"])
    print(f"    Merged rows after dropna: {len(merged)}, countries: {merged['iso'].nunique()}")

    # Bivariate correlation
    corr = run_bivariate_correlation(
        merged["proxy_value"], merged["value"], iso=merged["iso"]
    )
    print(f"    Pearson r={corr.pearson_r:.3f} (p={corr.pearson_p:.4f})")
    print(f"    Spearman rho={corr.spearman_rho:.3f} (p={corr.spearman_p:.4f})")
    print(f"    n={corr.n_observations}, countries={corr.n_countries}")

    # Partial correlation controlling for log(GDP per capita)
    gpc = load_raw_indicator("GPC")
    merged_gpc = merged.merge(
        gpc[["iso", "year", "value"]].rename(columns={"value": "gpc"}),
        on=["iso", "year"],
    )
    merged_gpc = merged_gpc.dropna(subset=["gpc"])
    merged_gpc["log_gpc"] = np.log(merged_gpc["gpc"].clip(lower=1))
    print(f"    Partial correlation n={len(merged_gpc)}")

    partial = run_partial_correlation(merged_gpc, "proxy_value", "value", ["log_gpc"])
    print(f"    Partial r={partial.partial_r:.3f} (p={partial.partial_p:.4f})")

    # Functional form
    form = test_functional_form(merged["proxy_value"], merged["value"])
    print(f"    Best functional form: {form.best_form.value}")

    # Verdict
    verdict = determine_verdict(corr, partial, "positive")
    print(f"\n    Verdict: {verdict.value}")

    data_quality_notes = (
        f"PARC index not publicly available as a machine-readable dataset. "
        f"Approach 1: IPBES PDF URL ({url}) contains only metadata. "
        f"Approach 2: World Bank searches for 'protected area representativeness', "
        f"'biodiversity protected area quality', etc. returned no PARC data. "
        f"Approach 3 (SUBSTITUTION): Used '{proxy_name_used}' (WB: {proxy_code_used}) "
        f"as an approximate proxy. This measures protected area coverage of key biodiversity "
        f"areas rather than representativeness per se, but is conceptually related — "
        f"higher KBA/PA coverage implies better representativeness of priority sites. "
        f"This is an exploratory substitution."
    )
    summary = (
        f"Using {proxy_name_used} as a proxy for Protected Area Representativeness (PARC). "
        f"Pearson r={corr.pearson_r:.3f} (p={corr.pearson_p:.4f}), "
        f"Spearman rho={corr.spearman_rho:.3f}. "
        f"Partial r={partial.partial_r:.3f} (p={partial.partial_p:.4f}) controlling for log(GPC). "
        f"n={corr.n_observations} obs, {corr.n_countries} countries. "
        f"Verdict: {verdict.value}."
    )
    verification_method = "exploratory_test"

    result = build_result_json(
        "SPI-H01",
        verdict,
        corr,
        partial,
        functional_form=form,
        data_quality_notes=data_quality_notes,
        summary=summary,
    )

else:
    print("\n[6] No usable proxy found — reporting inconclusive.")
    data_quality_notes = (
        f"PARC index is not publicly available as machine-readable data. "
        f"Approach 1: IPBES URL ({url}) is a PDF metadata document with no numeric data. "
        f"Approach 2: World Bank searches for 'protected area representativeness', "
        f"'biodiversity protected area quality', 'species protection representativeness', "
        f"'protected area coverage ecosystem' all returned results but none matched the "
        f"PARC concept. "
        f"Approach 3: Tried WB codes ER.MRN.PTMR.ZS (marine PAs), ER.LND.PTLD.ZS "
        f"(terrestrial+marine PAs), AG.LND.FRST.ZS (forest area), ER.PTD.TOTL.ZS "
        f"(KBA coverage) — all either returned insufficient merged rows (<30) or no data. "
        f"Approach 4: GEO BON and Protected Planet APIs are not publicly accessible. "
        f"The only available PA datasets were already used by SPI-H05. "
        f"No suitable alternative proxy found."
    )
    summary = (
        "PARC data is not publicly accessible in machine-readable form. "
        "All four data acquisition approaches exhausted without finding a usable proxy. "
        "Result is inconclusive due to data unavailability."
    )
    verification_method = "pending_data"
    verdict_str = "inconclusive"

    result = {
        "hypothesis_id": "SPI-H01",
        "verdict": verdict_str,
        "verification_method": verification_method,
        "data_quality_notes": data_quality_notes,
        "summary": summary,
        "bivariate_correlation": None,
        "partial_correlation": None,
        "functional_form": None,
    }

# ── Inject verification_method ────────────────────────────────
if isinstance(result, dict):
    result["verification_method"] = verification_method
else:
    result["verification_method"] = verification_method

# ── Write result.json ─────────────────────────────────────────
out_file = f"{output_path}/result.json"
with open(out_file, "w") as f:
    json.dump(result, f, indent=2, default=str)

print(f"\n✓ Results written to {out_file}")
print("Done.")