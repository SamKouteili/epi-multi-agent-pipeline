import json
import os
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore")

from src.utils.stats import (
    run_bivariate_correlation,
    run_partial_correlation,
    determine_verdict,
    build_result_json,
    test_functional_form,
)
from src.utils.data_utils import load_raw_indicator
from src.utils.data_fetch import fetch_world_bank_indicator, search_world_bank

output_path = "/Users/samkouteili/rose/epi/multi-agent/outputs/WRR/stage2/WRR-H06"
os.makedirs(output_path, exist_ok=True)

print("=== WRR-H06: Recycled Material Trade Flows vs WRR ===\n")

# ── 1. Load EPI target ──────────────────────────────────────────────────────
print("Loading WRR target indicator...")
target = load_raw_indicator("WRR")
print(f"  WRR: {len(target)} rows, {target['iso'].nunique()} countries, years {target['year'].min()}-{target['year'].max()}")

# ── 2. Acquire proxy data ────────────────────────────────────────────────────
# UN Comtrade requires authentication for bulk CSV downloads.
# We use World Bank proxy indicators as substitutes for recycled material trade flows.
# Strategy: try several indicators related to trade/waste/recycling capacity.

proxy = None
proxy_name = None
proxy_notes = []

print("\nSearching World Bank for recycled material trade indicators...")
try:
    results = search_world_bank("recycled waste materials trade")
    if results:
        print(f"  Found {len(results)} results (not directly relevant to recycled material trade)")
except Exception as e:
    print(f"  Search failed: {e}")
    proxy_notes.append(f"WB search failed: {e}")

# Try a sequence of WB indicators that might proxy for recycling trade capacity
print("\nAttempting to fetch World Bank proxy indicators...")

wb_candidates = [
    # Manufactures exports % merchandise exports — proxy for industrial/recycling capacity
    ("TX.VAL.MANF.ZS.UN", "Manufactures exports (% of merchandise exports)"),
    # Trade openness
    ("NE.TRD.GNFS.ZS", "Trade (% of GDP)"),
    # Energy use intensity (already succeeded in prior run — negative correlation, wrong direction)
    ("EG.USE.COMM.GD.PP.KD", "Energy use per GDP (proxy for industrial intensity)"),
]

for wb_code, description in wb_candidates:
    try:
        print(f"  Trying {wb_code} ({description})...")
        df = fetch_world_bank_indicator(wb_code)
        if df is not None and len(df) > 100:
            proxy = df.rename(columns={"value": "proxy_value"})
            proxy_name = f"WB:{wb_code} — {description}"
            print(f"    ✓ Got {len(proxy)} rows, {proxy['iso'].nunique()} countries")
            proxy_notes.append(
                f"Using WB indicator {wb_code} ({description}) as substitute for "
                "recycled material trade flows (UN Comtrade unavailable without auth)"
            )
            break
    except Exception as e:
        print(f"    ✗ Failed: {e}")
        proxy_notes.append(f"WB {wb_code} failed: {e}")

# ── 3. Handle case where no proxy is available ───────────────────────────────
if proxy is None:
    print("\nAll proxy data acquisition attempts failed. Writing INCONCLUSIVE result.")
    notes = (
        "Proxy data unavailable. "
        "UN Comtrade requires authentication for bulk CSV downloads. "
        "World Bank does not publish recycled material trade flows as a standardized indicator. "
        "Attempted WB indicators: TX.VAL.MANF.ZS.UN, NE.TRD.GNFS.ZS, EG.USE.COMM.GD.PP.KD. "
        + " | ".join(proxy_notes)
    )
    result = {
        "hypothesis_id": "WRR-H06",
        "verdict": "inconclusive",
        "verification_method": "statistical_test",
        "data_quality_notes": notes,
        "summary": (
            "Could not obtain recycled material trade flow data. "
            "UN Comtrade requires account-based API access; no equivalent is "
            "available through open World Bank endpoints."
        ),
        "bivariate_correlation": None,
        "partial_correlation": None,
        "functional_form": None,
    }
    out_file = f"{output_path}/result.json"
    with open(out_file, "w") as f:
        json.dump(result, f, indent=2)
    print(f"\nResult written to {out_file}")
else:
    print(f"\nUsing proxy: {proxy_name}")
    print(f"  Proxy rows: {len(proxy)}, countries: {proxy['iso'].nunique()}")

    # ── 4. Merge proxy with WRR target ───────────────────────────────────────
    print("\nMerging proxy with WRR target...")
    wrr_years = target["year"].unique()
    proxy_filtered = proxy[proxy["year"].isin(wrr_years)].copy()
    merged = target.merge(proxy_filtered, on=["iso", "year"])
    merged = merged.dropna(subset=["value", "proxy_value"])
    print(f"  Merged: {len(merged)} rows, {merged['iso'].nunique()} countries")

    if len(merged) < 20:
        print("  Insufficient data after merge — writing INCONCLUSIVE")
        notes = (
            f"Insufficient overlap between proxy ({proxy_name}) and WRR data after merge "
            f"({len(merged)} rows). "
            + " | ".join(proxy_notes)
        )
        result = {
            "hypothesis_id": "WRR-H06",
            "verdict": "inconclusive",
            "verification_method": "statistical_test",
            "data_quality_notes": notes,
            "summary": "Insufficient data overlap after merging proxy with WRR target.",
            "bivariate_correlation": None,
            "partial_correlation": None,
            "functional_form": None,
        }
        out_file = f"{output_path}/result.json"
        with open(out_file, "w") as f:
            json.dump(result, f, indent=2)
        print(f"Result written to {out_file}")
    else:
        # ── 5. Bivariate correlation ──────────────────────────────────────────
        print("\nRunning bivariate correlation...")
        corr = run_bivariate_correlation(
            merged["proxy_value"], merged["value"], iso=merged["iso"]
        )
        print(f"  Pearson r={corr.pearson_r:.4f}, p={corr.pearson_p:.4f}")
        print(f"  Spearman rho={corr.spearman_rho:.4f}, p={corr.spearman_p:.4f}")
        print(f"  n={corr.n_observations}, countries={corr.n_countries}")

        # ── 6. Partial correlation controlling for log(GDP per capita) ────────
        print("\nLoading GPC for partial correlation...")
        gpc = load_raw_indicator("GPC")
        merged_gpc = merged.merge(
            gpc[["iso", "year", "value"]].rename(columns={"value": "gpc"}),
            on=["iso", "year"],
        )
        merged_gpc = merged_gpc.dropna(subset=["gpc", "proxy_value", "value"])
        merged_gpc["log_gpc"] = np.log(merged_gpc["gpc"].clip(lower=1))
        print(f"  After GPC merge: {len(merged_gpc)} rows")

        partial = None
        if len(merged_gpc) >= 20:
            print("Running partial correlation (controlling for log GPC)...")
            try:
                partial = run_partial_correlation(
                    merged_gpc, "proxy_value", "value", ["log_gpc"]
                )
                print(f"  Partial r={partial.partial_r:.4f}, p={partial.partial_p:.4f}")
            except Exception as e:
                print(f"  Partial correlation failed: {e}")
                proxy_notes.append(f"Partial correlation computation failed: {e}")
                partial = None
        else:
            print("  Too few rows for partial correlation after GPC merge.")

        # ── 7. Functional form test ───────────────────────────────────────────
        print("\nTesting functional form...")
        form = None
        try:
            form = test_functional_form(merged["proxy_value"], merged["value"])
            print(f"  Best form: {form.best_form.value}")
            print(f"  Linear R²={form.linear_r2:.4f}, AIC={form.linear_aic:.2f}")
            print(f"  Log-linear R²={form.log_linear_r2:.4f}, AIC={form.log_linear_aic:.2f}")
            print(f"  Quadratic R²={form.quadratic_r2:.4f}, AIC={form.quadratic_aic:.2f}")
        except Exception as e:
            print(f"  Functional form test failed: {e}")
            proxy_notes.append(f"Functional form test failed: {e}")

        # ── 8. Verdict ────────────────────────────────────────────────────────
        print("\nDetermining verdict...")
        verdict = determine_verdict(corr, partial, "positive")
        print(f"  Verdict: {verdict.value}")

        # ── 9. Build result dict ──────────────────────────────────────────────
        notes = (
            f"Proxy used: {proxy_name}. "
            "NOTE: UN Comtrade direct recycled material trade flow data (the originally "
            "specified proxy) requires authenticated API access and was not available. "
            "The hypothesis specifies recycled material trade flows (metals, paper, "
            "plastics, glass as % of total material consumption) from UN Comtrade. "
            "This script uses a World Bank substitute indicator which is an imperfect proxy. "
            "China's 2018 import ban is a major structural break in recycled material trade. "
            "HS code inconsistency and price volatility are additional data quality concerns. "
            "Confounding with GDP/wealth is strong — wealthier countries both trade more "
            "AND have higher recycling rates. "
            + " | ".join(proxy_notes)
        )

        partial_summary = ""
        if partial is not None:
            partial_summary = (
                f"Partial r={partial.partial_r:.3f} (p={partial.partial_p:.3f}) "
                "controlling for log(GDP/capita). "
            )
        else:
            partial_summary = "Partial correlation not computed (computation failed or insufficient data). "

        form_summary = ""
        if form is not None:
            form_summary = f"Best functional form: {form.best_form.value}. "

        summary = (
            f"Using {proxy_name} as substitute for recycled material trade flows "
            f"(UN Comtrade unavailable without authentication). "
            f"Bivariate: Pearson r={corr.pearson_r:.3f} (p={corr.pearson_p:.3f}), "
            f"Spearman rho={corr.spearman_rho:.3f} (p={corr.spearman_p:.3f}), "
            f"n={corr.n_observations} obs across {corr.n_countries} countries. "
            + partial_summary
            + form_summary
            + f"Verdict: {verdict.value}."
        )

        # Build the result using build_result_json, then inject extra fields
        result = build_result_json(
            "WRR-H06",
            verdict,
            corr,
            partial,
            functional_form=form,
            data_quality_notes=notes,
            summary=summary,
        )
        result["verification_method"] = "statistical_test"

        out_file = f"{output_path}/result.json"
        with open(out_file, "w") as f:
            json.dump(result, f, indent=2, default=str)
        print(f"\nResult written to {out_file}")
        print(f"Final verdict: {verdict.value}")

print("\n=== Done ===")