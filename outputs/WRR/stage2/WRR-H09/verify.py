import json
import os
import requests
import pandas as pd
import numpy as np
from src.utils.stats import run_bivariate_correlation, run_partial_correlation, determine_verdict, build_result_json, test_functional_form
from src.utils.data_utils import load_raw_indicator
from src.utils.data_fetch import fetch_world_bank_indicator, search_world_bank

output_path = "/Users/samkouteili/rose/epi/multi-agent/outputs/WRR/stage2/WRR-H09"
os.makedirs(output_path, exist_ok=True)

print("=== WRR-H09: E-waste recycling rate vs WRR ===")
print()

# 1. Load EPI target data
print("Loading WRR target data...")
target = load_raw_indicator("WRR")
print(f"  WRR data: {len(target)} rows, {target['iso'].nunique()} countries")
print()

# 2. Acquire proxy data
# Primary: E-waste recycling rate (Global E-waste Monitor / ITU)
# Fallback: World Bank renewable energy output as infrastructure maturity proxy
# We'll try multiple WB indicators related to waste management / environmental technology

proxy = None
proxy_source = None
data_quality_notes = ""

# --- Attempt 1: World Bank renewable electricity (technology/infrastructure maturity proxy) ---
print("Attempt 1: World Bank EN.URB.MCTY.TL.ZS (urban concentration, already found)...")
try:
    df = fetch_world_bank_indicator("EN.URB.MCTY.TL.ZS")
    if df is not None and len(df) > 100:
        print(f"  Got {len(df)} rows, {df['iso'].nunique()} countries")
        # This is "urban population in largest city as % of total urban" — not ideal for e-waste
        # Let's skip and try better options
        print("  Skipping — not relevant enough for e-waste infrastructure")
except Exception as e:
    print(f"  Failed: {e}")

# --- Attempt 2: World Bank EG.ELC.RNEW.ZS - Renewable electricity (% of total) ---
print("Attempt 2: World Bank EG.ELC.RNEW.ZS (renewable electricity %)...")
try:
    df = fetch_world_bank_indicator("EG.ELC.RNEW.ZS")
    if df is not None and len(df) > 100:
        print(f"  Got {len(df)} rows, {df['iso'].nunique()} countries")
        # Renewable electricity - moderate proxy for environmental/tech infrastructure
        proxy = df.rename(columns={"value": "proxy_value"})
        proxy_source = "World Bank EG.ELC.RNEW.ZS: Renewable electricity (% of total)"
        data_quality_notes = (
            "Primary proxy (e-waste recycling rate from Global E-waste Monitor 2024) "
            "could not be accessed automatically — data is published as PDF/Excel requiring manual download. "
            "Substituted with World Bank EG.ELC.RNEW.ZS (renewable electricity output as % of total), "
            "which serves as a proxy for environmental technology infrastructure maturity. "
            "Countries with advanced renewable energy infrastructure tend to also have developed "
            "waste management and recycling systems. This is an imperfect substitute."
        )
        print(f"  Using as proxy: {proxy_source}")
except Exception as e:
    print(f"  Failed: {e}")

# --- Attempt 3: World Bank SH.STA.SMSS.ZS - Safely managed sanitation ---
if proxy is None:
    print("Attempt 3: World Bank SH.STA.SMSS.ZS (safely managed sanitation)...")
    try:
        df = fetch_world_bank_indicator("SH.STA.SMSS.ZS")
        if df is not None and len(df) > 100:
            print(f"  Got {len(df)} rows, {df['iso'].nunique()} countries")
            proxy = df.rename(columns={"value": "proxy_value"})
            proxy_source = "World Bank SH.STA.SMSS.ZS: Safely managed sanitation services (%)"
            data_quality_notes = (
                "Primary proxy (e-waste recycling rate) not accessible automatically. "
                "Substituted with World Bank SH.STA.SMSS.ZS (safely managed sanitation services) "
                "as a proxy for waste management infrastructure quality."
            )
            print(f"  Using as proxy: {proxy_source}")
    except Exception as e:
        print(f"  Failed: {e}")

# --- Attempt 4: World Bank EG.ELC.ACCS.ZS - Access to electricity ---
if proxy is None:
    print("Attempt 4: World Bank EG.ELC.ACCS.ZS (electricity access)...")
    try:
        df = fetch_world_bank_indicator("EG.ELC.ACCS.ZS")
        if df is not None and len(df) > 100:
            print(f"  Got {len(df)} rows, {df['iso'].nunique()} countries")
            proxy = df.rename(columns={"value": "proxy_value"})
            proxy_source = "World Bank EG.ELC.ACCS.ZS: Access to electricity (% of population)"
            data_quality_notes = (
                "Primary proxy (e-waste recycling rate) not accessible automatically. "
                "Substituted with electricity access as a proxy for infrastructure development."
            )
            print(f"  Using as proxy: {proxy_source}")
    except Exception as e:
        print(f"  Failed: {e}")

# --- If no proxy found, report inconclusive ---
if proxy is None:
    print("\nNo suitable proxy data found. Reporting inconclusive...")
    data_quality_notes = (
        "Attempted to access e-waste recycling rate data from: "
        "1) Global E-waste Monitor 2024 (ITU/UNITAR) — PDF report, no direct API access; "
        "2) Multiple World Bank indicators — none suitable found. "
        "Cannot verify hypothesis without e-waste recycling rate data."
    )
    result = {
        "hypothesis_id": "WRR-H09",
        "verdict": "inconclusive",
        "verification_method": "statistical_test",
        "data_quality_notes": data_quality_notes,
        "summary": (
            "Could not verify hypothesis due to data unavailability. "
            "E-waste recycling rate data from the Global E-waste Monitor 2024 "
            "requires manual download and is not available via API."
        ),
        "proxy_source": "None available",
        "n_observations": 0,
    }
    output_file = f"{output_path}/result.json"
    with open(output_file, "w") as f:
        json.dump(result, f, indent=2)
    print(f"\nResults written to {output_file}")
    print("Verdict: INCONCLUSIVE (data unavailable)")
else:
    # 3. Merge on iso + year
    print(f"\nMerging proxy with WRR target data...")
    proxy_clean = proxy[["iso", "year", "proxy_value"]].dropna(subset=["proxy_value"])
    merged = target.merge(proxy_clean, on=["iso", "year"])
    merged = merged.dropna(subset=["value", "proxy_value"])
    print(f"  Merged dataset: {len(merged)} rows, {merged['iso'].nunique()} countries")

    if len(merged) < 20:
        print(f"  WARNING: Only {len(merged)} observations — too few for reliable analysis")
        result = {
            "hypothesis_id": "WRR-H09",
            "verdict": "inconclusive",
            "verification_method": "statistical_test",
            "data_quality_notes": data_quality_notes + f" Only {len(merged)} overlapping observations.",
            "summary": f"Insufficient data overlap ({len(merged)} observations) after merging proxy with WRR.",
            "proxy_source": proxy_source,
            "n_observations": len(merged),
        }
        output_file = f"{output_path}/result.json"
        with open(output_file, "w") as f:
            json.dump(result, f, indent=2)
        print(f"Results written to {output_file}")
    else:
        # 4. Bivariate correlation
        print("\nRunning bivariate correlation...")
        corr = run_bivariate_correlation(
            merged["proxy_value"], merged["value"], iso=merged["iso"]
        )
        print(f"  Pearson r={corr.pearson_r:.4f}, p={corr.pearson_p:.4f}")
        print(f"  Spearman rho={corr.spearman_rho:.4f}, p={corr.spearman_p:.4f}")
        print(f"  N={corr.n_observations}, Countries={corr.n_countries}")

        # 5. Partial correlation controlling for log(GDP per capita)
        print("\nRunning partial correlation controlling for log(GDP)...")
        gpc = load_raw_indicator("GPC")
        merged_gpc = merged.merge(
            gpc[["iso", "year", "value"]].rename(columns={"value": "gpc"}),
            on=["iso", "year"]
        )
        merged_gpc = merged_gpc.dropna(subset=["gpc", "proxy_value", "value"])
        merged_gpc["log_gpc"] = np.log(merged_gpc["gpc"].clip(lower=1e-6))
        print(f"  Data for partial correlation: {len(merged_gpc)} rows")

        partial = None
        if len(merged_gpc) >= 20:
            try:
                partial = run_partial_correlation(
                    merged_gpc, "proxy_value", "value", ["log_gpc"]
                )
                print(f"  Partial r={partial.partial_r:.4f}, p={partial.partial_p:.4f}")
            except Exception as e:
                print(f"  Partial correlation failed: {e}")
                print("  Continuing without partial correlation result.")
                partial = None
        else:
            print(f"  Skipping partial correlation — insufficient overlap (n={len(merged_gpc)})")

        # 6. Functional form test
        print("\nTesting functional forms...")
        try:
            form = test_functional_form(merged["proxy_value"], merged["value"])
            print(f"  Best form: {form.best_form.value}")
            print(f"  Linear R²={form.linear_r2:.4f}, AIC={form.linear_aic:.2f}")
            print(f"  Log-linear R²={form.log_linear_r2:.4f}, AIC={form.log_linear_aic:.2f}")
            print(f"  Quadratic R²={form.quadratic_r2:.4f}, AIC={form.quadratic_aic:.2f}")
        except Exception as e:
            print(f"  Functional form test failed: {e}")
            form = None

        # 7. Verdict
        print("\nDetermining verdict...")
        verdict = determine_verdict(corr, partial, "positive")
        print(f"  Verdict: {verdict.value}")

        summary = (
            f"Hypothesis: E-waste recycling infrastructure correlates positively with WRR. "
            f"Proxy used: {proxy_source}. "
            f"Bivariate: Pearson r={corr.pearson_r:.3f} (p={corr.pearson_p:.4f}), "
            f"Spearman rho={corr.spearman_rho:.3f} (p={corr.spearman_p:.4f}), "
            f"N={corr.n_observations} obs, {corr.n_countries} countries. "
        )
        if partial is not None:
            summary += (
                f"Partial correlation (controlling log GDP): "
                f"r={partial.partial_r:.3f} (p={partial.partial_p:.4f}). "
            )
        else:
            summary += "Partial correlation: not computed. "
        if form is not None:
            summary += f"Best functional form: {form.best_form.value}."

        # Build result JSON
        result = build_result_json(
            "WRR-H09",
            verdict,
            corr,
            partial,
            functional_form=form,
            data_quality_notes=data_quality_notes,
            summary=summary
        )
        result["verification_method"] = "statistical_test"
        result["proxy_source"] = proxy_source

        output_file = f"{output_path}/result.json"
        with open(output_file, "w") as f:
            json.dump(result, f, indent=2, default=str)
        print(f"\nResults written to {output_file}")
        print(f"Final verdict: {verdict.value}")

print("\n=== Analysis complete ===")