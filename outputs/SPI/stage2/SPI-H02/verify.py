"""
SPI-H02: Verify hypothesis that Local Biodiversity Intactness Index (LBII)
correlates positively with Species Protection Index (SPI).

The primary LBII data source is a raster/GeoTIFF from GEO BON / UN Biodiversity Lab.
We attempt multiple fallback proxies for LBII.
"""

import json
import os
import numpy as np
import pandas as pd
import requests

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
)

output_path = "/Users/samkouteili/rose/epi/multi-agent/outputs/SPI/stage2/SPI-H02"
os.makedirs(output_path, exist_ok=True)

print("=" * 60)
print("SPI-H02: LBII vs Species Protection Index")
print("=" * 60)

# -------------------------------------------------------------------
# 1. Load EPI target data
# -------------------------------------------------------------------
print("\n[1] Loading SPI target indicator...")
target = load_raw_indicator("SPI")
print(f"    SPI data shape: {target.shape}")
print(f"    Countries: {target['iso'].nunique()}")
print(f"    Years available: {sorted(target['year'].unique())}")

# Use most recent year per country to maximize coverage
target_latest = (
    target.dropna(subset=["value"])
    .sort_values("year")
    .groupby("iso")
    .last()
    .reset_index()[["iso", "year", "value"]]
)
print(f"    Latest-year SPI: {len(target_latest)} countries")

# -------------------------------------------------------------------
# 2. Attempt to acquire LBII / biodiversity intactness proxy data
# -------------------------------------------------------------------
print("\n[2] Attempting to acquire LBII proxy data...")

proxy = None
proxy_source_desc = ""
proxy_notes = []

# --- Attempt A: EN.CLC.MDAT.ZS — mean protected area in important biodiversity sites ---
print("    [A] Trying EN.CLC.MDAT.ZS (protected area in important biodiversity sites)...")
try:
    df_a = fetch_world_bank_indicator("EN.CLC.MDAT.ZS")
    if df_a is not None and len(df_a) > 50:
        # Use latest value per country
        df_a_latest = (
            df_a.dropna(subset=["value"])
            .sort_values("year")
            .groupby("iso")
            .last()
            .reset_index()[["iso", "value"]]
            .rename(columns={"value": "proxy_value"})
        )
        if len(df_a_latest) >= 50:
            proxy = df_a_latest
            proxy_source_desc = "EN.CLC.MDAT.ZS (mean area protected in terrestrial sites important to biodiversity)"
            proxy_notes.append(f"Used WB indicator EN.CLC.MDAT.ZS as biodiversity protection proxy (n={len(proxy)}).")
            print(f"    SUCCESS: {len(proxy)} countries")
        else:
            print(f"    Too few countries: {len(df_a_latest)}")
    else:
        print(f"    Insufficient data")
except Exception as e:
    print(f"    Failed: {e}")

# --- Attempt B: ER.PTD.TOTL.ZS — terrestrial protected areas % ---
if proxy is None:
    print("    [B] Trying ER.PTD.TOTL.ZS (terrestrial protected areas %)...")
    try:
        df_b = fetch_world_bank_indicator("ER.PTD.TOTL.ZS")
        if df_b is not None and len(df_b) > 100:
            df_b_latest = (
                df_b.dropna(subset=["value"])
                .sort_values("year")
                .groupby("iso")
                .last()
                .reset_index()[["iso", "value"]]
                .rename(columns={"value": "proxy_value"})
            )
            if len(df_b_latest) >= 50:
                proxy = df_b_latest
                proxy_source_desc = "ER.PTD.TOTL.ZS (terrestrial protected areas % of total land area)"
                proxy_notes.append(f"Used WB ER.PTD.TOTL.ZS as biodiversity proxy (n={len(proxy)}).")
                print(f"    SUCCESS: {len(proxy)} countries")
            else:
                print(f"    Too few countries: {len(df_b_latest)}")
        else:
            print(f"    Insufficient data")
    except Exception as e:
        print(f"    Failed: {e}")

# --- Attempt C: AG.LND.FRST.ZS — forest area % (positive proxy for intactness) ---
if proxy is None:
    print("    [C] Trying AG.LND.FRST.ZS (forest area % as intactness proxy)...")
    try:
        df_c = fetch_world_bank_indicator("AG.LND.FRST.ZS")
        if df_c is not None and len(df_c) > 100:
            df_c_latest = (
                df_c.dropna(subset=["value"])
                .sort_values("year")
                .groupby("iso")
                .last()
                .reset_index()[["iso", "value"]]
                .rename(columns={"value": "proxy_value"})
            )
            if len(df_c_latest) >= 50:
                proxy = df_c_latest
                proxy_source_desc = "AG.LND.FRST.ZS (forest area % of land area, positive intactness proxy)"
                proxy_notes.append(f"Used WB AG.LND.FRST.ZS forest coverage as LBII proxy (n={len(proxy)}).")
                print(f"    SUCCESS: {len(proxy)} countries")
            else:
                print(f"    Too few countries: {len(df_c_latest)}")
        else:
            print(f"    Insufficient data")
    except Exception as e:
        print(f"    Failed: {e}")

# --- Attempt D: AG.LND.AGRI.ZS — inverse of agricultural land (intactness proxy) ---
if proxy is None:
    print("    [D] Trying inverse of AG.LND.AGRI.ZS (100 - agricultural land %)...")
    try:
        df_d = fetch_world_bank_indicator("AG.LND.AGRI.ZS")
        if df_d is not None and len(df_d) > 200:
            df_d_latest = (
                df_d.dropna(subset=["value"])
                .sort_values("year")
                .groupby("iso")
                .last()
                .reset_index()[["iso", "value"]]
            )
            df_d_latest["proxy_value"] = 100 - df_d_latest["value"]
            df_d_latest = df_d_latest[["iso", "proxy_value"]]
            if len(df_d_latest) >= 50:
                proxy = df_d_latest
                proxy_source_desc = "100 - AG.LND.AGRI.ZS (inverse agricultural land, rough intactness proxy)"
                proxy_notes.append(
                    f"Used (100 - agricultural land %) as rough inverse proxy for land use pressure (n={len(proxy)})."
                )
                print(f"    SUCCESS: {len(proxy)} countries")
            else:
                print(f"    Too few countries: {len(df_d_latest)}")
        else:
            print(f"    Insufficient data")
    except Exception as e:
        print(f"    Failed: {e}")

# -------------------------------------------------------------------
# 3. Merge proxy with SPI
# -------------------------------------------------------------------
if proxy is None:
    print("\n[!] All proxy acquisition attempts failed — writing INCONCLUSIVE result.")
    result = {
        "hypothesis_id": "SPI-H02",
        "verdict": "inconclusive",
        "verification_method": "statistical_test",
        "data_quality_notes": (
            "LBII (Local Biodiversity Intactness Index) is distributed as a 1km raster/GeoTIFF. "
            "No tabular country-level version was accessible via World Bank API, direct URL downloads, "
            "or WHO GHO. All attempts to find substitute indicators also failed."
        ),
        "summary": (
            "Unable to verify SPI-H02. LBII is available only as a global raster product and "
            "no country-level aggregated version was found via accessible APIs or open data repositories."
        ),
    }
    out_file = f"{output_path}/result.json"
    with open(out_file, "w") as f:
        json.dump(result, f, indent=2)
    print(f"    Saved to {out_file}")

else:
    print(f"\n[3] Merging proxy with SPI (latest year per country)...")
    print(f"    Proxy countries: {len(proxy)}")
    print(f"    SPI latest-year countries: {len(target_latest)}")

    # Merge on iso only (both are latest-value cross-sections)
    merged = target_latest.merge(proxy, on="iso")
    merged = merged.dropna(subset=["value", "proxy_value"])
    print(f"    Merged: {len(merged)} countries")
    print(f"    SPI range: {merged['value'].min():.2f} – {merged['value'].max():.2f}")
    print(f"    Proxy range: {merged['proxy_value'].min():.2f} – {merged['proxy_value'].max():.2f}")

    if len(merged) < 10:
        print("[!] Insufficient merged data — writing INCONCLUSIVE.")
        result = {
            "hypothesis_id": "SPI-H02",
            "verdict": "inconclusive",
            "verification_method": "statistical_test",
            "data_quality_notes": "; ".join(proxy_notes) + f" Only {len(merged)} matched observations.",
            "summary": "Insufficient matched data for statistical testing.",
        }
        out_file = f"{output_path}/result.json"
        with open(out_file, "w") as f:
            json.dump(result, f, indent=2)
        print(f"    Saved to {out_file}")

    else:
        # ---------------------------------------------------------------
        # 4. Bivariate correlation
        # ---------------------------------------------------------------
        print("\n[4] Running bivariate correlation...")
        corr = run_bivariate_correlation(
            merged["proxy_value"], merged["value"], iso=merged["iso"]
        )
        print(f"    Pearson r={corr.pearson_r:.4f}, p={corr.pearson_p:.4e}")
        print(f"    Spearman rho={corr.spearman_rho:.4f}, p={corr.spearman_p:.4e}")
        print(f"    N={corr.n_observations}, Countries={corr.n_countries}")

        # ---------------------------------------------------------------
        # 5. Partial correlation controlling for log(GDP per capita)
        # ---------------------------------------------------------------
        print("\n[5] Running partial correlation controlling for log(GDP per capita)...")
        gpc = load_raw_indicator("GPC")
        gpc_latest = (
            gpc.dropna(subset=["value"])
            .sort_values("year")
            .groupby("iso")
            .last()
            .reset_index()[["iso", "value"]]
            .rename(columns={"value": "gpc"})
        )
        merged_gpc = merged.merge(gpc_latest, on="iso")
        merged_gpc = merged_gpc.dropna(subset=["gpc"])
        merged_gpc["log_gpc"] = np.log(merged_gpc["gpc"].clip(lower=1))
        print(f"    N after GPC merge: {len(merged_gpc)}")

        partial = None
        if len(merged_gpc) >= 20:
            partial = run_partial_correlation(merged_gpc, "proxy_value", "value", ["log_gpc"])
            print(f"    Partial r={partial.partial_r:.4f}, p={partial.partial_p:.4e}")
        else:
            print("    Insufficient data for partial correlation")

        # ---------------------------------------------------------------
        # 6. Functional form test
        # ---------------------------------------------------------------
        print("\n[6] Testing functional form...")
        form = test_functional_form(merged["proxy_value"], merged["value"])
        print(f"    Best form: {form.best_form.value}")
        print(f"    Linear     R²={form.linear_r2:.4f}, AIC={form.linear_aic:.2f}")

        # Guard against None values when log-linear or quadratic fits fail
        if form.log_linear_r2 is not None and form.log_linear_aic is not None:
            print(f"    Log-linear R²={form.log_linear_r2:.4f}, AIC={form.log_linear_aic:.2f}")
        else:
            print("    Log-linear fit not available (possibly non-positive proxy values)")

        if form.quadratic_r2 is not None and form.quadratic_aic is not None:
            print(f"    Quadratic  R²={form.quadratic_r2:.4f}, AIC={form.quadratic_aic:.2f}")
        else:
            print("    Quadratic fit not available")

        # ---------------------------------------------------------------
        # 7. Verdict
        # ---------------------------------------------------------------
        print("\n[7] Determining verdict...")
        verdict = determine_verdict(corr, partial, "positive")
        print(f"    Verdict: {verdict.value}")

        # ---------------------------------------------------------------
        # 8. Build and save result
        # ---------------------------------------------------------------
        data_notes = (
            f"Proxy used: {proxy_source_desc}. "
            + "; ".join(proxy_notes)
            + " True LBII (raster product at 1km resolution) was not accessible as country-level "
            "tabular data. A World Bank substitute indicator was used instead. "
            "Taxonomic bias toward vertebrates/plants is noted in PREDICTS; "
            "this substitute does not fully capture local biodiversity intactness."
        )

        summary = (
            f"Using '{proxy_source_desc}' as a substitute for LBII, "
            f"bivariate correlation with SPI is r={corr.pearson_r:.3f} "
            f"(p={corr.pearson_p:.3e}, n={corr.n_observations} countries). "
            f"Spearman rho={corr.spearman_rho:.3f} (p={corr.spearman_p:.3e}). "
        )
        if partial is not None:
            summary += (
                f"After controlling for log(GDP/capita): partial r={partial.partial_r:.3f} "
                f"(p={partial.partial_p:.3e}). "
            )
        summary += (
            f"Best functional form: {form.best_form.value}. "
            f"Verdict: {verdict.value}. "
            "Note: Results reflect the substitute proxy, not true LBII."
        )

        result = build_result_json(
            "SPI-H02",
            verdict,
            corr,
            partial,
            functional_form=form,
            data_quality_notes=data_notes,
            summary=summary,
        )
        result["verification_method"] = "statistical_test"

        out_file = f"{output_path}/result.json"
        with open(out_file, "w") as f:
            json.dump(result, f, indent=2)
        print(f"\n[8] Result saved to {out_file}")
        print(json.dumps(result, indent=2))

print("\nDone.")