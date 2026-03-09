import json
import os
import pandas as pd
import numpy as np
import requests

from src.utils.stats import (
    run_bivariate_correlation,
    run_partial_correlation,
    determine_verdict,
    build_result_json,
    test_functional_form,
)
from src.utils.data_utils import load_raw_indicator
from src.utils.data_fetch import fetch_world_bank_indicator, search_world_bank

# Output directory
output_path = "/Users/samkouteili/rose/epi/multi-agent/outputs/SPI/stage2/SPI-H04"
os.makedirs(output_path, exist_ok=True)

print("=== SPI-H04: Red List Index (RLI) vs Species Protection Index (SPI) ===\n")

# 1. Load EPI target data
print("Loading SPI target indicator...")
target = load_raw_indicator("SPI")
print(f"  SPI data: {len(target)} rows, {target['iso'].nunique()} countries")

# 2. Try to get Red List Index data
# The RLI is tracked by the World Bank as SDG indicator 15.5.1
# World Bank code: ER.RSK.LST.DELTOT (may vary) — let's try known codes

rli_proxy = None
data_quality_notes = ""

# Try World Bank first — RLI is published as WB indicator
print("\nAttempting to fetch Red List Index from World Bank (ER.RSK.LST.DELTOT)...")
try:
    rli_proxy = fetch_world_bank_indicator("ER.RSK.LST.DELTOT")
    if rli_proxy is not None and len(rli_proxy) > 0:
        print(f"  Fetched {len(rli_proxy)} rows from ER.RSK.LST.DELTOT")
    else:
        print("  No data returned from ER.RSK.LST.DELTOT")
        rli_proxy = None
except Exception as e:
    print(f"  Failed: {e}")
    rli_proxy = None

if rli_proxy is None or len(rli_proxy) == 0:
    # Search for the correct WB code
    print("\nSearching World Bank for Red List Index...")
    try:
        results = search_world_bank("red list index species survival")
        print(f"  Search results: {results}")
    except Exception as e:
        print(f"  Search failed: {e}")

    # Try alternative known WB indicator codes for RLI
    candidate_codes = [
        "ER.RSK.LST.DELTOT",
        "EN.HP.FLRI.RELI",  # unlikely but try
        "15.5.1",
    ]
    for code in candidate_codes:
        print(f"\nTrying WB indicator: {code}...")
        try:
            df = fetch_world_bank_indicator(code)
            if df is not None and len(df) > 0:
                print(f"  SUCCESS: {len(df)} rows")
                rli_proxy = df
                data_quality_notes += f"Used World Bank indicator {code} as proxy for RLI. "
                break
        except Exception as e:
            print(f"  Failed: {e}")

if rli_proxy is None or len(rli_proxy) == 0:
    # Try downloading from a known open data source
    # Our World in Data publishes RLI data as CSV
    print("\nTrying Our World in Data RLI dataset...")
    owid_url = "https://raw.githubusercontent.com/owid/owid-datasets/master/datasets/IUCN%20Red%20List%20Index/IUCN%20Red%20List%20Index.csv"
    try:
        resp = requests.get(owid_url, timeout=30)
        if resp.status_code == 200:
            from io import StringIO
            df_raw = pd.read_csv(StringIO(resp.text))
            print(f"  Downloaded OWID RLI data: {df_raw.shape}")
            print(f"  Columns: {list(df_raw.columns)}")
            # OWID format typically has Entity, Code, Year, and value column
            # Identify value column
            val_col = [c for c in df_raw.columns if c not in ["Entity", "Code", "Year"]]
            if val_col:
                df_raw = df_raw.rename(columns={
                    "Code": "iso",
                    "Year": "year",
                    val_col[0]: "proxy_value"
                })
                rli_proxy = df_raw[["iso", "year", "proxy_value"]].dropna()
                rli_proxy["year"] = rli_proxy["year"].astype(int)
                print(f"  Processed: {len(rli_proxy)} rows, {rli_proxy['iso'].nunique()} countries")
                data_quality_notes += "Used OWID RLI dataset from GitHub. "
        else:
            print(f"  HTTP {resp.status_code}")
    except Exception as e:
        print(f"  Failed: {e}")

if rli_proxy is None or len(rli_proxy) == 0:
    # Try alternative OWID URL
    print("\nTrying alternative OWID RLI URL...")
    alt_urls = [
        "https://ourworldindata.org/grapher/red-list-index.csv?tab=chart",
        "https://raw.githubusercontent.com/owid/owid-datasets/master/datasets/Red%20List%20Index%20-%20IUCN%20(2023)/Red%20List%20Index%20-%20IUCN%20(2023).csv",
    ]
    for url in alt_urls:
        try:
            resp = requests.get(url, timeout=30)
            if resp.status_code == 200:
                from io import StringIO
                df_raw = pd.read_csv(StringIO(resp.text))
                print(f"  Downloaded from {url}: {df_raw.shape}")
                print(f"  Columns: {list(df_raw.columns[:10])}")
                # Try to parse
                iso_col = next((c for c in df_raw.columns if c.lower() in ["code", "iso", "country_code"]), None)
                year_col = next((c for c in df_raw.columns if c.lower() == "year"), None)
                val_cols = [c for c in df_raw.columns if c.lower() not in ["entity", "code", "year", "iso", "country", "country_code"]]
                if iso_col and year_col and val_cols:
                    df_raw = df_raw.rename(columns={iso_col: "iso", year_col: "year", val_cols[0]: "proxy_value"})
                    rli_proxy = df_raw[["iso", "year", "proxy_value"]].dropna()
                    rli_proxy["year"] = rli_proxy["year"].astype(int)
                    print(f"  Processed: {len(rli_proxy)} rows")
                    data_quality_notes += f"Used RLI data from {url}. "
                    break
        except Exception as e:
            print(f"  Failed: {e}")

if rli_proxy is None or len(rli_proxy) == 0:
    # One more attempt - World Bank SDG 15.5.1
    print("\nSearching for SDG 15.5.1 (RLI) on World Bank...")
    try:
        results = search_world_bank("IUCN red list threatened species")
        print(f"  Results: {results}")
    except Exception as e:
        print(f"  {e}")

    try:
        # World Bank API direct call
        url = "https://api.worldbank.org/v2/indicator?q=red+list+index&format=json&per_page=20"
        resp = requests.get(url, timeout=20)
        if resp.status_code == 200:
            data = resp.json()
            if len(data) > 1:
                indicators = data[1]
                for ind in indicators[:5]:
                    print(f"  Found indicator: {ind.get('id')} — {ind.get('name')}")
    except Exception as e:
        print(f"  {e}")

# Check if we have data
if rli_proxy is None or len(rli_proxy) == 0:
    print("\n⚠️  Could not retrieve RLI data from any source.")
    print("Writing inconclusive result...")

    result = {
        "hypothesis_id": "SPI-H04",
        "verdict": "inconclusive",
        "verification_method": "statistical_test",
        "data_quality_notes": (
            "Could not retrieve Red List Index (RLI) data from IUCN, World Bank, or Our World in Data. "
            "Attempted: World Bank indicators ER.RSK.LST.DELTOT and variants, "
            "OWID GitHub repository, and direct World Bank API search. "
            "The RLI (SDG 15.5.1) may require direct IUCN API access or manual download. "
            "No statistical test could be performed."
        ),
        "summary": (
            "Hypothesis SPI-H04 could not be verified due to data unavailability. "
            "The Red List Index measures average extinction risk across assessed species "
            "and is expected to correlate positively with SPI (Species Protection Index). "
            "A 5-10 year lag is hypothesized due to time needed for protected areas to "
            "benefit species populations."
        ),
    }

    out_file = f"{output_path}/result.json"
    with open(out_file, "w") as f:
        json.dump(result, f, indent=2)
    print(f"\nResult written to {out_file}")

else:
    # We have RLI data — proceed with analysis
    print(f"\nRLI proxy data: {len(rli_proxy)} rows, {rli_proxy['iso'].nunique()} countries")
    print(f"RLI year range: {rli_proxy['year'].min()} - {rli_proxy['year'].max()}")
    print(f"RLI value range: {rli_proxy['proxy_value'].min():.4f} - {rli_proxy['proxy_value'].max():.4f}")

    # Rename proxy column if needed
    if "value" in rli_proxy.columns and "proxy_value" not in rli_proxy.columns:
        rli_proxy = rli_proxy.rename(columns={"value": "proxy_value"})

    # 3. Merge on iso + year
    print("\nMerging SPI and RLI data...")
    merged = target.merge(rli_proxy[["iso", "year", "proxy_value"]], on=["iso", "year"])
    merged = merged.dropna(subset=["value", "proxy_value"])
    print(f"  Merged dataset: {len(merged)} rows, {merged['iso'].nunique()} countries")

    if len(merged) < 10:
        print("⚠️  Insufficient data for statistical analysis after merging.")
        result = {
            "hypothesis_id": "SPI-H04",
            "verdict": "inconclusive",
            "verification_method": "statistical_test",
            "data_quality_notes": (
                f"RLI data was retrieved ({len(rli_proxy)} rows) but only {len(merged)} "
                "observations remained after merging with SPI data. Insufficient for analysis. "
                + data_quality_notes
            ),
            "summary": "Insufficient overlap between RLI and SPI data for statistical testing.",
        }
        out_file = f"{output_path}/result.json"
        with open(out_file, "w") as f:
            json.dump(result, f, indent=2)
        print(f"Result written to {out_file}")
    else:
        # 4. Bivariate correlation
        print("\nComputing bivariate correlation...")
        corr = run_bivariate_correlation(
            merged["proxy_value"], merged["value"], iso=merged["iso"]
        )
        print(f"  Pearson r={corr.pearson_r:.4f}, p={corr.pearson_p:.4f}")
        print(f"  Spearman rho={corr.spearman_rho:.4f}, p={corr.spearman_p:.4f}")
        print(f"  n={corr.n_observations}, n_countries={corr.n_countries}")

        # 5. Partial correlation controlling for log(GDP per capita)
        print("\nLoading GPC for partial correlation...")
        gpc = load_raw_indicator("GPC")
        merged_gpc = merged.merge(
            gpc[["iso", "year", "value"]].rename(columns={"value": "gpc"}),
            on=["iso", "year"]
        )
        merged_gpc = merged_gpc.dropna(subset=["gpc"])
        merged_gpc["log_gpc"] = np.log(merged_gpc["gpc"].replace(0, np.nan))
        merged_gpc = merged_gpc.dropna(subset=["log_gpc"])
        print(f"  After merging GPC: {len(merged_gpc)} rows")

        partial = None
        if len(merged_gpc) >= 20:
            partial = run_partial_correlation(merged_gpc, "proxy_value", "value", ["log_gpc"])
            print(f"  Partial r={partial.partial_r:.4f}, p={partial.partial_p:.4f}")
        else:
            print("  Insufficient data for partial correlation")

        # 6. Functional form test
        print("\nTesting functional form...")
        form = test_functional_form(merged["proxy_value"], merged["value"])
        print(f"  Best form: {form.best_form.value}")
        print(f"  Linear R²={form.linear_r2:.4f}, AIC={form.linear_aic:.2f}")
        print(f"  Log-linear R²={form.log_linear_r2:.4f}, AIC={form.log_linear_aic:.2f}")
        print(f"  Quadratic R²={form.quadratic_r2:.4f}, AIC={form.quadratic_aic:.2f}")

        # 7. Verdict
        print("\nDetermining verdict...")
        verdict = determine_verdict(corr, partial, "positive")
        print(f"  Verdict: {verdict.value}")

        data_quality_notes += (
            "RLI data sourced from OWID/World Bank. "
            "RLI ranges 0 (all extinct) to 1 (no species extinct). "
            "Higher RLI = better outcomes, consistent with positive direction hypothesis. "
            "Note: a 5-10 year lag effect was hypothesized but not explicitly tested here "
            "(contemporaneous matching used). Data Deficient species are excluded from RLI, "
            "biasing toward well-known vertebrates."
        )

        result = build_result_json(
            "SPI-H04",
            verdict,
            corr,
            partial,
            functional_form=form,
            data_quality_notes=data_quality_notes,
            summary=(
                f"The Red List Index (RLI) shows a {verdict.value} correlation with the "
                f"Species Protection Index (SPI). Pearson r={corr.pearson_r:.3f} (p={corr.pearson_p:.4f}), "
                f"Spearman rho={corr.spearman_rho:.3f} (p={corr.spearman_p:.4f}), "
                f"n={corr.n_observations} observations across {corr.n_countries} countries. "
                + (f"Partial correlation controlling for log(GDP/capita): r={partial.partial_r:.3f} (p={partial.partial_p:.4f}). " if partial else "")
                + f"Best functional form: {form.best_form.value}. "
                "The RLI measures average extinction risk and is expected to correlate positively "
                "with SPI (Species Protection Index), as well-protected areas should reduce "
                "extinction pressure. A lag effect of 5-10 years may attenuate contemporaneous correlations."
            ),
        )
        result["verification_method"] = "statistical_test"

        out_file = f"{output_path}/result.json"
        with open(out_file, "w") as f:
            json.dump(result, f, indent=2)
        print(f"\nResult written to {out_file}")
        print(f"Final verdict: {verdict.value}")