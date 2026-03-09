import json
import os
import numpy as np
import pandas as pd
import requests
import traceback

from src.utils.stats import (
    run_bivariate_correlation,
    run_partial_correlation,
    determine_verdict,
    build_result_json,
    test_functional_form,
)
from src.utils.data_utils import load_raw_indicator
from src.utils.data_fetch import fetch_world_bank_indicator, search_world_bank

OUTPUT_DIR = "/Users/samkouteili/rose/epi/multi-agent/outputs/OEB/stage2/OEB-H07/"
os.makedirs(OUTPUT_DIR, exist_ok=True)

HYPOTHESIS_ID = "OEB-H07"
EXPECTED_DIRECTION = "positive"

print("=== OEB-H07: Solar Radiation Intensity → OEB Verification ===\n")

# ── 1. Load EPI target ──────────────────────────────────────────────────────
print("Loading OEB target indicator...")
target = load_raw_indicator("OEB")
print(f"  OEB rows: {len(target)}, countries: {target['iso'].nunique()}")

# ── 2. Country centroids ────────────────────────────────────────────────────
# Hard-coded approximate centroids for ~180 countries
COUNTRY_CENTROIDS = {
    "AFG": (33.93, 67.71), "ALB": (41.15, 20.17), "DZA": (28.03, 1.66),
    "AGO": (-11.20, 17.87), "ARG": (-38.42, -63.62), "ARM": (40.07, 45.04),
    "AUS": (-25.27, 133.78), "AUT": (47.52, 14.55), "AZE": (40.14, 47.58),
    "BHS": (25.03, -77.40), "BHR": (26.00, 50.55), "BGD": (23.68, 90.36),
    "BLR": (53.71, 27.95), "BEL": (50.50, 4.47), "BLZ": (17.19, -88.50),
    "BEN": (9.31, 2.32), "BTN": (27.51, 90.43), "BOL": (-16.29, -63.59),
    "BIH": (43.92, 17.68), "BWA": (-22.33, 24.68), "BRA": (-14.24, -51.93),
    "BRN": (4.54, 114.73), "BGR": (42.73, 25.49), "BFA": (12.36, -1.56),
    "BDI": (-3.37, 29.92), "CPV": (16.00, -24.01), "KHM": (12.57, 104.99),
    "CMR": (3.85, 11.50), "CAN": (56.13, -106.35), "CAF": (6.61, 20.94),
    "TCD": (15.45, 18.73), "CHL": (-35.68, -71.54), "CHN": (35.86, 104.20),
    "COL": (4.57, -74.30), "COM": (-11.88, 43.87), "COG": (-0.23, 15.83),
    "COD": (-4.04, 21.76), "CRI": (9.75, -83.75), "CIV": (7.54, -5.55),
    "HRV": (45.10, 15.20), "CUB": (21.52, -77.78), "CYP": (35.13, 33.43),
    "CZE": (49.82, 15.47), "DNK": (56.26, 9.50), "DJI": (11.83, 42.59),
    "DOM": (18.74, -70.16), "ECU": (-1.83, -78.18), "EGY": (26.82, 30.80),
    "SLV": (13.79, -88.90), "GNQ": (1.65, 10.27), "ERI": (15.18, 39.78),
    "EST": (58.60, 25.01), "SWZ": (-26.52, 31.47), "ETH": (9.15, 40.49),
    "FJI": (-16.58, 179.41), "FIN": (61.92, 25.75), "FRA": (46.23, 2.21),
    "GAB": (-0.80, 11.61), "GMB": (13.44, -15.31), "GEO": (42.32, 43.36),
    "DEU": (51.17, 10.45), "GHA": (7.95, -1.02), "GRC": (39.07, 21.82),
    "GTM": (15.78, -90.23), "GIN": (11.00, -10.94), "GNB": (11.80, -15.18),
    "GUY": (4.86, -58.93), "HTI": (18.97, -72.29), "HND": (15.20, -86.24),
    "HUN": (47.16, 19.50), "ISL": (64.96, -19.02), "IND": (20.59, 78.96),
    "IDN": (-0.79, 113.92), "IRN": (32.43, 53.69), "IRQ": (33.22, 43.68),
    "IRL": (53.41, -8.24), "ISR": (31.05, 34.85), "ITA": (41.87, 12.57),
    "JAM": (18.11, -77.30), "JPN": (36.20, 138.25), "JOR": (30.59, 36.24),
    "KAZ": (48.02, 66.92), "KEN": (-0.02, 37.91), "PRK": (40.34, 127.51),
    "KOR": (35.91, 127.77), "KWT": (29.31, 47.48), "KGZ": (41.20, 74.77),
    "LAO": (19.86, 102.50), "LVA": (56.88, 24.60), "LBN": (33.85, 35.86),
    "LSO": (-29.61, 28.23), "LBR": (6.43, -9.43), "LBY": (26.34, 17.23),
    "LTU": (55.17, 23.88), "LUX": (49.82, 6.13), "MDG": (-18.77, 46.87),
    "MWI": (-13.25, 34.30), "MYS": (4.21, 109.43), "MDV": (3.20, 73.22),
    "MLI": (17.57, -3.99), "MLT": (35.94, 14.38), "MRT": (21.01, -10.94),
    "MUS": (-20.35, 57.55), "MEX": (23.63, -102.55), "MDA": (47.41, 28.37),
    "MNG": (46.86, 103.85), "MNE": (42.71, 19.37), "MAR": (31.79, -7.09),
    "MOZ": (-18.67, 35.53), "MMR": (16.87, 96.41), "NAM": (-22.96, 18.49),
    "NPL": (28.39, 84.12), "NLD": (52.13, 5.29), "NZL": (-40.90, 174.89),
    "NIC": (12.87, -85.21), "NER": (17.61, 8.08), "NGA": (9.08, 8.68),
    "MKD": (41.61, 21.75), "NOR": (60.47, 8.47), "OMN": (21.51, 55.92),
    "PAK": (30.38, 69.35), "PAN": (8.54, -80.78), "PNG": (-6.31, 143.96),
    "PRY": (-23.44, -58.44), "PER": (-9.19, -75.02), "PHL": (12.88, 121.77),
    "POL": (51.92, 19.15), "PRT": (39.40, -8.22), "QAT": (25.35, 51.18),
    "ROU": (45.94, 24.97), "RUS": (61.52, 105.32), "RWA": (-1.94, 29.87),
    "SAU": (23.89, 45.08), "SEN": (14.50, -14.45), "SRB": (44.02, 21.01),
    "SLE": (8.46, -11.78), "SVK": (48.67, 19.70), "SVN": (46.15, 14.99),
    "SOM": (5.15, 46.20), "ZAF": (-30.56, 22.94), "SSD": (6.88, 31.31),
    "ESP": (40.46, -3.75), "LKA": (7.87, 80.77), "SDN": (12.86, 30.22),
    "SUR": (3.92, -56.03), "SWE": (60.13, 18.64), "CHE": (46.82, 8.23),
    "SYR": (34.80, 38.60), "TJK": (38.86, 71.28), "TZA": (-6.37, 34.89),
    "THA": (15.87, 100.99), "TLS": (-8.87, 125.73), "TGO": (8.62, 0.82),
    "TTO": (10.69, -61.22), "TUN": (33.89, 9.54), "TUR": (38.96, 35.24),
    "TKM": (38.97, 59.56), "UGA": (1.37, 32.29), "UKR": (48.38, 31.17),
    "ARE": (23.42, 53.85), "GBR": (55.38, -3.44), "USA": (37.09, -95.71),
    "URY": (-32.52, -55.77), "UZB": (41.38, 64.59), "VEN": (6.42, -66.59),
    "VNM": (14.06, 108.28), "YEM": (15.55, 48.52), "ZMB": (-13.13, 27.85),
    "ZWE": (-19.02, 29.15),
}

print(f"  Using {len(COUNTRY_CENTROIDS)} country centroids")

# ── 3. Try NASA POWER API ───────────────────────────────────────────────────
print("\nAttempting NASA POWER API for solar irradiance...")

def fetch_nasa_power_solar(iso, lat, lon, start_year=2003, end_year=2022):
    """Fetch annual surface SW irradiance from NASA POWER for a single location."""
    url = "https://power.larc.nasa.gov/api/temporal/annual/point"
    params = {
        "parameters": "ALLSKY_SFC_SW_DWN",
        "community": "RE",
        "longitude": round(lon, 4),
        "latitude": round(lat, 4),
        "start": start_year,
        "end": end_year,
        "format": "JSON",
    }
    try:
        r = requests.get(url, params=params, timeout=45)
        r.raise_for_status()
        data = r.json()
        annual_data = data["properties"]["parameter"]["ALLSKY_SFC_SW_DWN"]
        rows = []
        for year_str, val in annual_data.items():
            try:
                yr = int(year_str)
                if val is not None and val != -999.0 and not np.isnan(float(val)):
                    rows.append({"iso": iso, "year": yr, "proxy_value": float(val)})
            except Exception:
                pass
        return rows
    except Exception as e:
        return []

# Test with a few countries
test_isos = ["BRA", "USA", "DEU", "NGA", "AUS"]
print(f"  Testing API with {test_isos}...")
test_rows = []
for iso in test_isos:
    if iso in COUNTRY_CENTROIDS:
        lat, lon = COUNTRY_CENTROIDS[iso]
        rows = fetch_nasa_power_solar(iso, lat, lon, 2003, 2005)
        test_rows.extend(rows)
        print(f"    {iso}: {len(rows)} records")

api_worked = len(test_rows) > 0
proxy_rows = []

if api_worked:
    print(f"  NASA POWER API working! Fetching all countries...")
    failed = 0
    for idx, (iso, (lat, lon)) in enumerate(COUNTRY_CENTROIDS.items()):
        rows = fetch_nasa_power_solar(iso, lat, lon, 2003, 2022)
        proxy_rows.extend(rows)
        if len(rows) == 0:
            failed += 1
        if (idx + 1) % 30 == 0:
            print(f"    Progress: {idx+1}/{len(COUNTRY_CENTROIDS)}, records: {len(proxy_rows)}, failed: {failed}")
    
    proxy = pd.DataFrame(proxy_rows)
    print(f"  Solar data: {len(proxy)} records, {proxy['iso'].nunique()} countries")
    data_quality_note = (
        "Solar irradiance data (ALLSKY_SFC_SW_DWN, W/m²) from NASA POWER REST API, "
        "CERES-derived, annual averages at country centroid coordinates, 2003-2022. "
        "CERES/NetCDF was not downloaded directly; NASA POWER provides equivalent data via API."
    )
else:
    print("  NASA POWER API unavailable — using latitude-based solar proxy.")
    # ── Fallback: latitude-based geometric solar irradiance approximation ──
    # Annual mean insolation at top of atmosphere varies as cos(latitude).
    # Surface SW ≈ 200 + 200*cos(|lat| * pi/180) is a reasonable first-order proxy.
    lat_rows = []
    for iso, (lat, lon) in COUNTRY_CENTROIDS.items():
        lat_rad = abs(lat) * np.pi / 180
        sw_proxy = 200.0 + 200.0 * np.cos(lat_rad)
        for yr in range(2003, 2023):
            lat_rows.append({"iso": iso, "year": yr, "proxy_value": sw_proxy})
    proxy = pd.DataFrame(lat_rows)
    print(f"  Latitude-based proxy: {len(proxy)} records, {proxy['iso'].nunique()} countries")
    data_quality_note = (
        "NASA POWER API was unavailable. "
        "World Bank search found no direct solar irradiance indicator. "
        "Fell back to latitude-derived geometric solar proxy: SW ≈ 200 + 200*cos(|lat|) W/m². "
        "This is a deterministic first-order approximation of annual mean surface irradiance. "
        "Results reflect the latitude–ozone relationship rather than measured irradiance."
    )

# ── 4. Merge ────────────────────────────────────────────────────────────────
print("\nMerging proxy with OEB target...")
merged = target.merge(proxy, on=["iso", "year"])
merged = merged.dropna(subset=["value", "proxy_value"])
print(f"  Merged rows: {len(merged)}, countries: {merged['iso'].nunique()}")
print(f"  OEB range: {merged['value'].min():.4f} – {merged['value'].max():.4f}")
print(f"  Proxy range: {merged['proxy_value'].min():.2f} – {merged['proxy_value'].max():.2f}")

if len(merged) < 20:
    print("INSUFFICIENT DATA — writing inconclusive result.")
    result = build_result_json(
        HYPOTHESIS_ID,
        "inconclusive",
        None, None,
        functional_form=None,
        data_quality_notes=f"Insufficient merged data ({len(merged)} rows). " + data_quality_note,
        summary="Could not obtain sufficient solar irradiance data to test the hypothesis.",
        verification_method="statistical_test",
    )
    out_path = os.path.join(OUTPUT_DIR, "result.json")
    with open(out_path, "w") as f:
        json.dump(result, f, indent=2)
    print(f"Result written to {out_path}")
    import sys; sys.exit(0)

# ── 5. Bivariate correlation ─────────────────────────────────────────────────
print("\nRunning bivariate correlation...")
corr = run_bivariate_correlation(
    merged["proxy_value"], merged["value"], iso=merged["iso"]
)
print(f"  Pearson r={corr.pearson_r:.4f}, p={corr.pearson_p:.4e}")
print(f"  Spearman rho={corr.spearman_rho:.4f}, p={corr.spearman_p:.4e}")
print(f"  N observations={corr.n_observations}, N countries={corr.n_countries}")

# ── 6. Partial correlation controlling for log(GDP per capita) ──────────────
print("\nRunning partial correlation (controlling for log GPC)...")
gpc = load_raw_indicator("GPC")
merged_gpc = merged.merge(
    gpc[["iso", "year", "value"]].rename(columns={"value": "gpc"}),
    on=["iso", "year"]
)
merged_gpc = merged_gpc.dropna(subset=["gpc"])
merged_gpc = merged_gpc[merged_gpc["gpc"] > 0]
merged_gpc["log_gpc"] = np.log(merged_gpc["gpc"])
print(f"  Rows for partial correlation: {len(merged_gpc)}")

partial = run_partial_correlation(merged_gpc, "proxy_value", "value", ["log_gpc"])
print(f"  Partial r={partial.partial_r:.4f}, p={partial.partial_p:.4e}")

# ── 7. Functional form ───────────────────────────────────────────────────────
print("\nTesting functional form...")
form = test_functional_form(merged["proxy_value"], merged["value"])
print(f"  Best form: {form.best_form.value}")
print(f"  Linear    R²={form.linear_r2:.4f}, AIC={form.linear_aic:.2f}")
print(f"  Log-linear R²={form.log_linear_r2:.4f}, AIC={form.log_linear_aic:.2f}")
print(f"  Quadratic  R²={form.quadratic_r2:.4f}, AIC={form.quadratic_aic:.2f}")

# ── 8. Verdict ───────────────────────────────────────────────────────────────
print("\nDetermining verdict...")
from src.utils.stats import Verdict
verdict = determine_verdict(corr, partial, EXPECTED_DIRECTION)
print(f"  Verdict: {verdict.value}")

# ── 9. Build and save result ─────────────────────────────────────────────────
proxy_source = "NASA POWER API (ALLSKY_SFC_SW_DWN, W/m²)" if api_worked else "latitude-derived geometric proxy"
summary = (
    f"Tested solar radiation intensity ({proxy_source}) as a proxy for ozone exposure "
    f"in Key Biodiversity Areas (OEB). "
    f"Bivariate: Pearson r={corr.pearson_r:.3f} (p={corr.pearson_p:.3e}), "
    f"Spearman rho={corr.spearman_rho:.3f} (p={corr.spearman_p:.3e}). "
    f"Partial correlation controlling for log(GPC): r={partial.partial_r:.3f} (p={partial.partial_p:.3e}). "
    f"Best functional form: {form.best_form.value}. "
    f"Hypothesis predicts positive direction (higher solar → more photochemical ozone production). "
    f"N={corr.n_observations} obs across {corr.n_countries} countries."
)

result = build_result_json(
    HYPOTHESIS_ID,
    verdict,
    corr,
    partial,
    functional_form=form,
    data_quality_notes=data_quality_note,
    summary=summary,
    verification_method="statistical_test",
)

out_path = os.path.join(OUTPUT_DIR, "result.json")
with open(out_path, "w") as f:
    json.dump(result, f, indent=2)
print(f"\nResult written to {out_path}")
print(f"Final verdict: {verdict.value}")