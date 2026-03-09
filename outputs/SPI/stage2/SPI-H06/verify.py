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
    LOCAL_CONTROLS,
)

OUTPUT_DIR = "/Users/samkouteili/rose/epi/multi-agent/outputs/SPI/stage2/SPI-H06/"
os.makedirs(OUTPUT_DIR, exist_ok=True)

HYPOTHESIS_ID = "SPI-H06"
EXPECTED_DIRECTION = "negative"

# ── 1. Load EPI target ────────────────────────────────────────────────────────
print("Loading SPI target indicator...")
target = load_raw_indicator("SPI")
print(f"  SPI rows: {len(target)}, countries: {target['iso'].nunique()}")

# ── 2. Approach 1: Direct URL fetch ──────────────────────────────────────────
print("\nApproach 1: Trying direct URL fetch from MODIS page...")
url = "https://modis.gsfc.nasa.gov/sci_team/meetings/200101/Presentations/l2_townshend.pdf"
try:
    resp = requests.get(url, timeout=15)
    print(f"  Response status: {resp.status_code}, content-type: {resp.headers.get('content-type','?')}")
    print("  → This is a PDF presentation slide deck, not tabular data. Cannot parse as proxy data.")
except Exception as e:
    print(f"  → URL fetch failed: {e}")

# ── 3. Approach 2: Check local indicators ────────────────────────────────────
print("\nApproach 2: Checking local indicators...")
local_inds = list_local_indicators()
print(f"  Local indicators available: {local_inds}")

# ── 4. Approach 3: Search World Bank for fragmentation / land cover proxies ──
print("\nApproach 3: Searching World Bank for related indicators...")

queries = [
    "forest fragmentation landscape",
    "land cover change deforestation",
    "habitat loss forest area",
    "forest cover loss",
    "agricultural land expansion",
    "deforestation land use",
]

wb_results = {}
for q in queries:
    try:
        results = search_world_bank(q)
        if results:
            wb_results[q] = results[:5]
            print(f"  '{q}': {[r.get('id','?') + ' — ' + r.get('name','?') for r in results[:3]]}")
    except Exception as e:
        print(f"  '{q}' search error: {e}")

# ── 5. Try concrete WB indicators as fragmentation proxies ───────────────────
# Forest area (% of land area) — proxy: less forest = more fragmentation
# Agricultural land (% of land area) — proxy: more agriculture = more habitat loss/fragmentation
# Forest area change (annual % loss) — directly linked to fragmentation
print("\nFetching candidate proxy indicators from World Bank...")

proxy_candidates = {
    "AG.LND.FRST.ZS": "Forest area (% of land area)",
    "AG.LND.AGRI.ZS": "Agricultural land (% of land area)",
    "AG.LND.FRST.K2": "Forest area (sq. km)",
    "ER.LND.PTLD.ZS": "Terrestrial and marine protected areas (% of total territorial area)",
    "EN.CLC.MDAT.ZS": "Land area where elevation is below 5 meters (% of total land area)",
}

proxy_dfs = {}
for code, name in proxy_candidates.items():
    try:
        df = fetch_world_bank_indicator(code)
        if df is not None and len(df) > 100:
            proxy_dfs[code] = (df, name)
            print(f"  ✓ {code} ({name}): {len(df)} rows, {df['iso'].nunique()} countries")
        else:
            print(f"  ✗ {code}: insufficient data")
    except Exception as e:
        print(f"  ✗ {code} failed: {e}")

# ── 6. Pick best proxy: Forest area (% land area) as inverse fragmentation proxy
# Lower forest % → more fragmentation → lower SPI (so expected direction: positive correlation)
# But hypothesis says habitat fragmentation → negative SPI.
# We'll use agricultural land (%) as a direct fragmentation driver: MORE ag land = MORE fragmentation = LOWER SPI
# Expected direction: agricultural land negatively correlated with SPI → negative

best_code = None
best_name = None

# Prefer agricultural land as fragmentation driver
if "AG.LND.AGRI.ZS" in proxy_dfs:
    best_code = "AG.LND.AGRI.ZS"
    best_name = proxy_dfs[best_code][1]
    proxy_df = proxy_dfs[best_code][0].copy()
    proxy_df = proxy_df.rename(columns={"value": "proxy_value"})
    print(f"\nUsing '{best_name}' as fragmentation proxy (agricultural land expansion drives fragmentation).")
elif "AG.LND.FRST.ZS" in proxy_dfs:
    best_code = "AG.LND.FRST.ZS"
    best_name = proxy_dfs[best_code][1]
    proxy_df = proxy_dfs[best_code][0].copy()
    proxy_df = proxy_df.rename(columns={"value": "proxy_value"})
    print(f"\nUsing '{best_name}' as fragmentation proxy (forest cover loss → fragmentation).")
    print("  NOTE: direction flipped — more forest = less fragmentation, so correlation with SPI should be positive.")
    EXPECTED_DIRECTION = "positive"  # override for forest area
else:
    best_code = None
    print("\nNo suitable WB proxy found.")

if best_code is None:
    print("\nAll approaches exhausted. No usable proxy data found.")
    result = {
        "hypothesis_id": HYPOTHESIS_ID,
        "verdict": "inconclusive",
        "verification_method": "pending_data",
        "data_quality_notes": (
            "Attempted all 4 data acquisition approaches: "
            "(1) Direct URL fetch of MODIS PDF — not parseable tabular data. "
            "(2) Local indicators checked — none directly measure habitat fragmentation. "
            "(3) World Bank searches for 'forest fragmentation', 'land cover change', 'habitat loss', etc. — "
            "no direct fragmentation metrics (patch size, edge density, core area index) available. "
            "(4) WB indicator fetch attempts failed or returned insufficient data. "
            "True fragmentation metrics require raster processing (e.g., FRAGSTATS on MODIS/ESA land cover) "
            "and are not available as precomputed country-level statistics in any accessible API. "
            "Already-used proxies: LBII, SHI, IUCN Red List, protected areas (terrestrial), "
            "FAO pesticides, PARC indices."
        ),
        "summary": (
            "Habitat fragmentation metrics (patch size, edge density, core area index) require "
            "computational raster processing and are not available in any accessible API. "
            "The hypothesis cannot be verified without custom GIS analysis of MODIS/ESA land cover data."
        ),
    }
    out_path = os.path.join(OUTPUT_DIR, "result.json")
    with open(out_path, "w") as f:
        json.dump(result, f, indent=2)
    print(f"\nResult written to {out_path}")
    import sys
    sys.exit(0)

# ── 7. Merge with SPI target ──────────────────────────────────────────────────
print(f"\nMerging {best_name} proxy with SPI target...")
merged = target.merge(proxy_df[["iso", "year", "proxy_value"]], on=["iso", "year"])
merged = merged.dropna(subset=["proxy_value", "value"])
print(f"  Merged rows: {len(merged)}, countries: {merged['iso'].nunique()}")

if len(merged) < 20:
    print("  Insufficient overlapping data.")
    result = {
        "hypothesis_id": HYPOTHESIS_ID,
        "verdict": "inconclusive",
        "verification_method": "pending_data",
        "data_quality_notes": f"Insufficient overlapping data after merge (n={len(merged)}).",
        "summary": "Could not verify due to insufficient data coverage.",
    }
    out_path = os.path.join(OUTPUT_DIR, "result.json")
    with open(out_path, "w") as f:
        json.dump(result, f, indent=2)
    print(f"Result written to {out_path}")
    import sys
    sys.exit(0)

# ── 8. Bivariate correlation ──────────────────────────────────────────────────
print("\nRunning bivariate correlation...")
corr = run_bivariate_correlation(merged["proxy_value"], merged["value"], iso=merged["iso"])
print(f"  Pearson r={corr.pearson_r:.4f}, p={corr.pearson_p:.4e}")
print(f"  Spearman rho={corr.spearman_rho:.4f}, p={corr.spearman_p:.4e}")
print(f"  n={corr.n_observations}, n_countries={corr.n_countries}")

# ── 9. Partial correlation controlling for log(GDP per capita) ────────────────
print("\nLoading GPC control variable...")
gpc = load_raw_indicator("GPC")
merged_gpc = merged.merge(
    gpc[["iso", "year", "value"]].rename(columns={"value": "gpc"}),
    on=["iso", "year"]
)
merged_gpc = merged_gpc.dropna(subset=["gpc"])
merged_gpc["log_gpc"] = np.log(merged_gpc["gpc"].clip(lower=1e-6))
print(f"  Rows with GPC: {len(merged_gpc)}, countries: {merged_gpc['iso'].nunique()}")

partial = None
if len(merged_gpc) >= 20:
    print("Running partial correlation (controlling for log GPC)...")
    partial = run_partial_correlation(merged_gpc, "proxy_value", "value", ["log_gpc"])
    print(f"  Partial r={partial.partial_r:.4f}, p={partial.partial_p:.4e}")
else:
    print("  Insufficient data for partial correlation.")

# ── 10. Functional form test ──────────────────────────────────────────────────
print("\nTesting functional forms...")
form = test_functional_form(merged["proxy_value"], merged["value"])
print(f"  Best form: {form.best_form.value}")
print(f"  Linear R²={form.linear_r2:.4f}, Log-linear R²={form.log_linear_r2:.4f}, Quadratic R²={form.quadratic_r2:.4f}")

# ── 11. Verdict ───────────────────────────────────────────────────────────────
print("\nDetermining verdict...")
verdict = determine_verdict(corr, partial, EXPECTED_DIRECTION)
print(f"  Verdict: {verdict.value}")

# ── 12. Build and save result ─────────────────────────────────────────────────
data_quality_notes = (
    f"SUBSTITUTION: True habitat fragmentation metrics (patch size, edge density, core area index) "
    f"are not available as country-level statistics in any accessible API — they require raster "
    f"processing of MODIS/ESA land cover data. "
    f"Used '{best_name}' (WB: {best_code}) as an approximate proxy: higher agricultural land share "
    f"implies greater habitat conversion and fragmentation. "
    f"This is an indirect proxy that captures land-use pressure rather than landscape configuration directly. "
    f"Already-used proxies excluded: LBII, SHI, IUCN Red List, protected areas, FAO pesticides, PARC indices. "
    f"n={corr.n_observations} observations, {corr.n_countries} countries after merge."
)

summary = (
    f"Using agricultural land area (% of total land) as an indirect proxy for habitat fragmentation "
    f"(higher agricultural expansion → more habitat conversion and fragmentation → lower SPI). "
    f"Bivariate Pearson r={corr.pearson_r:.3f} (p={corr.pearson_p:.3e}), "
    f"Spearman rho={corr.spearman_rho:.3f} (p={corr.spearman_p:.3e}). "
    + (f"Partial r={partial.partial_r:.3f} (p={partial.partial_p:.3e}) controlling for log(GDP/capita). " if partial else "") +
    f"Best functional form: {form.best_form.value}. "
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

# Add verification_method
result["verification_method"] = "exploratory_test"

out_path = os.path.join(OUTPUT_DIR, "result.json")
with open(out_path, "w") as f:
    json.dump(result, f, indent=2)

print(f"\nResult written to {out_path}")
print(json.dumps(result, indent=2))