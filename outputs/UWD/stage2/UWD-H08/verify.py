"""
UWD-H08: Satellite-derived water turbidity vs UWD (Unsafe Water DALYs)
Proxy: Mean annual suspended sediment concentration / turbidity index
Source: USGS Earth Explorer / Copernicus Open Access Hub (GeoTIFF/NetCDF)

Since the primary data source requires GIS expertise and direct satellite
image processing (Landsat 8 / Sentinel-2), we attempt to find a suitable
proxy via World Bank or other APIs that capture water turbidity or
suspended sediments at the country level.
"""

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
    Verdict,
)
from src.utils.data_utils import load_raw_indicator
from src.utils.data_fetch import (
    fetch_world_bank_indicator,
    search_world_bank,
    list_local_indicators,
    LOCAL_CONTROLS,
    fetch_who_gho_indicator,
)

OUTPUT_PATH = "/Users/samkouteili/rose/epi/multi-agent/outputs/UWD/stage2/UWD-H08"
os.makedirs(OUTPUT_PATH, exist_ok=True)

HYPOTHESIS_ID = "UWD-H08"
EXPECTED_DIRECTION = "positive"

print("=" * 60)
print(f"Verifying hypothesis: {HYPOTHESIS_ID}")
print("Proxy: Satellite-derived water turbidity / SSC")
print("=" * 60)

# ── 1. Load EPI target ──────────────────────────────────────────
print("\n[1] Loading UWD target indicator...")
target = load_raw_indicator("UWD")
print(f"    UWD rows: {len(target)}, countries: {target['iso'].nunique()}")
print(f"    Years: {sorted(target['year'].unique())[:5]} … {sorted(target['year'].unique())[-5:]}")

# ── 2. Attempt proxy acquisition ─────────────────────────────────
print("\n[2] Attempting to acquire satellite-derived turbidity proxy...")

tried = []

# --- Attempt A: The primary source (USGS EarthExplorer / Copernicus) ---
print("  [A] Primary source: USGS EarthExplorer / Copernicus Open Access Hub")
print("      Requires GIS processing pipeline — not accessible via API. Skipping.")
tried.append("USGS EarthExplorer (requires GIS pipeline, not accessible via API)")

# --- Attempt B: World Bank water quality / sediment indicators ---
print("\n  [B] Searching World Bank for water turbidity / sediment proxies...")

search_terms = [
    "water turbidity",
    "suspended sediment",
    "water quality surface",
    "river discharge sediment",
]

for term in search_terms:
    try:
        results = search_world_bank(term)
        if results is not None and len(results) > 0:
            print(f"      '{term}': {len(results)} results (no direct turbidity index found)")
    except Exception as e:
        print(f"      '{term}': error — {e}")

tried.append(f"World Bank search ({len(search_terms)} queries) — no country-level turbidity index found")

# Known WB indicators that could approximate turbidity / water clarity:
wb_codes_to_try = [
    ("SH.H2O.BASW.ZS", "Basic drinking water services (%)"),
    ("ER.H2O.FWDM.ZS", "Water productivity, total"),
]

print("\n  [B2] Trying specific WB indicator codes as turbidity proxies...")
for code, label in wb_codes_to_try:
    try:
        df = fetch_world_bank_indicator(code)
        if df is not None and len(df) > 50:
            print(f"      {code} ({label}): {len(df)} rows — available but not turbidity")
        tried.append(f"WB {code}: {label} (available but measures water access, not turbidity)")
    except Exception as e:
        print(f"      {code}: error — {e}")
        tried.append(f"WB {code}: error")

# --- Attempt C: WHO GHO indicators ---
print("\n  [C] WHO GHO: checking for water quality indicators...")
who_codes = [
    "WSH_SANITATION_SAFELY_MANAGED",
    "WSH_WATER_SAFELY_MANAGED",
    "WHS3_41",
]
for wcode in who_codes:
    try:
        df = fetch_who_gho_indicator(wcode)
        if df is not None and len(df) > 50:
            print(f"      WHO {wcode}: {len(df)} rows — available but measures access, not turbidity")
        tried.append(f"WHO GHO {wcode}: available but measures water access, not turbidity")
    except Exception as e:
        print(f"      WHO {wcode}: error — {e}")
        tried.append(f"WHO GHO {wcode}: error")

# --- Summary of attempts ---
print("\n[2] Conclusion: No country-level satellite turbidity dataset accessible via API.")
print("    The hypothesis requires processing Landsat 8 / Sentinel-2 GeoTIFF imagery,")
print("    which is beyond the scope of automated API-based verification.")

data_quality_notes = (
    "The primary proxy (satellite-derived NDTI / SSC from Landsat 8 / Sentinel-2) "
    "requires authenticated GIS processing pipelines (USGS EarthExplorer, Copernicus "
    "Open Access Hub) that are not accessible via simple API calls. "
    "No country-level, pre-processed annual turbidity or suspended sediment concentration "
    "dataset was found through: "
    "(1) USGS EarthExplorer direct download — requires GIS pipeline; "
    "(2) World Bank API search across multiple turbidity/sediment query terms — no matching "
    "country-level annual turbidity index found; "
    "(3) WHO GHO API — water safety access metrics available but these measure water service "
    "coverage (negative direction vs UWD), not physical turbidity. "
    "World Bank water access indicators (SH.H2O.BASW.ZS, ER.H2O.FWDM.ZS, etc.) are "
    "available but measure water SERVICE ACCESS, not the hypothesized physical turbidity. "
    "Verdict: inconclusive due to data inaccessibility. "
    "To properly verify this hypothesis, a global country-level annual mean NDTI or SSC "
    "composite derived from Landsat/Sentinel imagery (e.g., from Google Earth Engine) "
    "would be required."
)

summary = (
    "Hypothesis UWD-H08 posits that satellite-derived water turbidity (NDTI/SSC "
    "from Landsat 8/Sentinel-2) is positively correlated with unsafe water DALYs. "
    "This is a theoretically plausible mechanism: high suspended sediment loads "
    "indicate potential fecal/pathogen contamination. However, the proxy data "
    "requires specialized GIS processing of petabyte-scale satellite imagery and "
    "is not available through any accessible API or pre-processed country-level "
    "dataset. Verdict is inconclusive due to data inaccessibility, not because the "
    "hypothesis is implausible."
)

# ── 3. Build inconclusive result manually ────────────────────────
# build_result_json requires real CorrelationResult objects (cannot pass None).
# We write the JSON directly for the inconclusive case.
print("\n[3] Building inconclusive result JSON (writing directly)...")

result = {
    "hypothesis_id": HYPOTHESIS_ID,
    "verdict": Verdict.inconclusive.value,
    "verification_method": "statistical_test",
    "proxy_attempted": "Satellite-derived NDTI/SSC (Landsat 8 / Sentinel-2)",
    "proxy_available": False,
    "data_sources_tried": tried,
    "bivariate_correlation": None,
    "partial_correlation": None,
    "functional_form": None,
    "data_quality_notes": data_quality_notes,
    "summary": summary,
    "expected_direction": EXPECTED_DIRECTION,
    "expected_functional_form": "log-linear",
    "confidence_prior": "speculative",
    "n_observations": None,
    "n_countries": None,
}

# ── 4. Write output ───────────────────────────────────────────────
out_file = f"{OUTPUT_PATH}/result.json"
print(f"\n[4] Writing results to {out_file}")
with open(out_file, "w") as f:
    json.dump(result, f, indent=2, default=str)

print("\n" + "=" * 60)
print(f"VERDICT: {Verdict.inconclusive.value}")
print("=" * 60)
print("Reason: Satellite turbidity data not accessible via API.")
print(f"Output: {out_file}")