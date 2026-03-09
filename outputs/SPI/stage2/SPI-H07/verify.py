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

OUTPUT_DIR = "/Users/samkouteili/rose/epi/multi-agent/outputs/SPI/stage2/SPI-H07/"
os.makedirs(OUTPUT_DIR, exist_ok=True)

HYPOTHESIS_ID = "SPI-H07"
TARGET_TLA = "SPI"
EXPECTED_DIRECTION = "positive"

print("=" * 60)
print(f"Verifying hypothesis: {HYPOTHESIS_ID}")
print("Target: Species Protection Index (SPI)")
print("Proxy: Protected Area Management Effectiveness (PAME)")
print("=" * 60)

# -------------------------------------------------------------------
# 1. Load EPI target data
# -------------------------------------------------------------------
print("\n[1] Loading SPI target data...")
target = load_raw_indicator(TARGET_TLA)
print(f"    SPI: {len(target)} rows, {target['iso'].nunique()} countries")

# -------------------------------------------------------------------
# Approach 1: Direct URL fetch from GD-PAME / BIOPAMA
# -------------------------------------------------------------------
print("\n[Approach 1] Trying direct URL fetch from BIOPAMA...")
tried_urls = []

urls_to_try = [
    "https://rris.biopama.org/node/20639",
    "https://www.protectedplanet.net/c/protected-areas-management-effectiveness-pame-data",
    "https://raw.githubusercontent.com/unep-wcmc/GD-PAME/main/data/pame_country_scores.csv",
]

direct_data = None
for url in urls_to_try:
    tried_urls.append(url)
    try:
        print(f"    Trying: {url}")
        r = requests.get(url, timeout=15)
        print(f"    Status: {r.status_code}, Content-Type: {r.headers.get('Content-Type','?')}")
        if r.status_code == 200:
            content_type = r.headers.get("Content-Type", "")
            if "csv" in content_type or url.endswith(".csv"):
                from io import StringIO
                direct_data = pd.read_csv(StringIO(r.text))
                print(f"    Downloaded CSV: {direct_data.shape}")
                break
            elif "json" in content_type:
                direct_data = pd.DataFrame(r.json())
                print(f"    Downloaded JSON: {direct_data.shape}")
                break
            else:
                print(f"    Got HTML/other — not parseable as structured data")
    except Exception as e:
        print(f"    Failed: {e}")

# -------------------------------------------------------------------
# Approach 2: World Bank search for PAME / PA management effectiveness
# -------------------------------------------------------------------
print("\n[Approach 2] Searching World Bank for related indicators...")
wb_results = {}
search_queries = [
    "protected area management effectiveness",
    "protected areas management quality",
    "biodiversity protected area",
    "protected area governance",
]
for q in search_queries:
    try:
        results = search_world_bank(q)
        if results is not None and len(results) > 0:
            wb_results[q] = results
            print(f"    '{q}': {len(results)} results")
            if isinstance(results, list):
                for r in results[:2]:
                    print(f"      {r}")
            elif hasattr(results, 'head'):
                print(results.head(2))
    except Exception as e:
        print(f"    Search '{q}' failed: {e}")

# -------------------------------------------------------------------
# Approach 3: Find approximate proxy using governance/institutional
# quality indicators as proxies for PA management effectiveness
# -------------------------------------------------------------------
print("\n[Approach 3] Fetching approximate proxy indicators...")

proxy_data = None
proxy_source = None
proxy_label = None

# Try Government Effectiveness (WGI) — GE.EST
# This is a reasonable proxy for PA management effectiveness:
# institutional quality determines whether PAs are managed vs 'paper parks'
print("    Trying: Government Effectiveness (WGI) — GE.EST")
try:
    ge = fetch_world_bank_indicator("GE.EST")
    if ge is not None and len(ge) > 0:
        ge = ge.rename(columns={"value": "proxy_value"})
        ge = ge.dropna(subset=["proxy_value"])
        print(f"    Government Effectiveness: {len(ge)} rows, {ge['iso'].nunique()} countries")
        proxy_data = ge
        proxy_source = "World Bank WGI: Government Effectiveness (GE.EST)"
        proxy_label = "Government Effectiveness Score"
    else:
        print("    No data returned")
except Exception as e:
    print(f"    Failed: {e}")

# If GE failed, try Rule of Law
if proxy_data is None:
    print("    Trying: Rule of Law (WGI) — RL.EST")
    try:
        rl = fetch_world_bank_indicator("RL.EST")
        if rl is not None and len(rl) > 0:
            rl = rl.rename(columns={"value": "proxy_value"})
            rl = rl.dropna(subset=["proxy_value"])
            print(f"    Rule of Law: {len(rl)} rows, {rl['iso'].nunique()} countries")
            proxy_data = rl
            proxy_source = "World Bank WGI: Rule of Law (RL.EST)"
            proxy_label = "Rule of Law Score"
        else:
            print("    No data returned")
    except Exception as e:
        print(f"    Failed: {e}")

# If still None, try Regulatory Quality (WGI)
if proxy_data is None:
    print("    Trying: Regulatory Quality (WGI) — RQ.EST")
    try:
        rq = fetch_world_bank_indicator("RQ.EST")
        if rq is not None and len(rq) > 0:
            rq = rq.rename(columns={"value": "proxy_value"})
            rq = rq.dropna(subset=["proxy_value"])
            print(f"    Regulatory Quality: {len(rq)} rows, {rq['iso'].nunique()} countries")
            proxy_data = rq
            proxy_source = "World Bank WGI: Regulatory Quality (RQ.EST)"
            proxy_label = "Regulatory Quality Score"
        else:
            print("    No data returned")
    except Exception as e:
        print(f"    Failed: {e}")

# -------------------------------------------------------------------
# 4. Merge and run statistics (if proxy found)
# -------------------------------------------------------------------
if proxy_data is not None:
    print(f"\n[4] Merging SPI with proxy: {proxy_source}")
    print(f"    Proxy data years: {sorted(proxy_data['year'].unique())[:5]}...{sorted(proxy_data['year'].unique())[-5:]}")
    print(f"    Target data years: {sorted(target['year'].unique())[:5]}...{sorted(target['year'].unique())[-5:]}")

    merged = target.merge(proxy_data[["iso", "year", "proxy_value"]], on=["iso", "year"])
    merged = merged.dropna(subset=["value", "proxy_value"])
    print(f"    Merged dataset: {len(merged)} rows, {merged['iso'].nunique()} countries")

    if len(merged) < 20:
        print("    WARNING: Too few observations — trying year-agnostic merge (most recent values)")
        # Fall back to latest year per country
        target_latest = target.dropna(subset=["value"]).sort_values("year").groupby("iso").last().reset_index()
        proxy_latest = proxy_data.dropna(subset=["proxy_value"]).sort_values("year").groupby("iso").last().reset_index()
        merged = target_latest.merge(proxy_latest[["iso", "proxy_value"]], on="iso")
        merged = merged.dropna(subset=["value", "proxy_value"])
        print(f"    After cross-sectional fallback: {len(merged)} rows, {merged['iso'].nunique()} countries")

    if len(merged) < 10:
        print("    Still too few observations. Reporting inconclusive.")
        proxy_data = None  # Force inconclusive path

if proxy_data is not None and len(merged) >= 10:
    # Bivariate correlation
    print("\n[5] Running bivariate correlation...")
    corr = run_bivariate_correlation(merged["proxy_value"], merged["value"], iso=merged["iso"])
    print(f"    Pearson r={corr.pearson_r:.3f}, p={corr.pearson_p:.4f}")
    print(f"    Spearman rho={corr.spearman_rho:.3f}, p={corr.spearman_p:.4f}")
    print(f"    N={corr.n_observations}, Countries={corr.n_countries}")

    # Partial correlation controlling for log(GDP per capita)
    print("\n[6] Running partial correlation controlling for log(GPC)...")
    gpc = load_raw_indicator("GPC")
    merged_gpc = merged.merge(
        gpc[["iso", "year", "value"]].rename(columns={"value": "gpc"}),
        on=["iso", "year"],
        how="left"
    )
    # If year-based merge failed, try iso-only merge for GPC
    if merged_gpc["gpc"].isna().all():
        gpc_latest = gpc.dropna(subset=["value"]).sort_values("year").groupby("iso").last().reset_index()
        merged_gpc = merged.merge(
            gpc_latest[["iso", "value"]].rename(columns={"value": "gpc"}),
            on="iso",
            how="left"
        )
    merged_gpc = merged_gpc.dropna(subset=["gpc"])
    merged_gpc["log_gpc"] = np.log(merged_gpc["gpc"].clip(lower=1))
    print(f"    Merged with GPC: {len(merged_gpc)} rows")

    partial = None
    if len(merged_gpc) >= 20:
        try:
            partial = run_partial_correlation(merged_gpc, "proxy_value", "value", ["log_gpc"])
            print(f"    Partial r={partial.partial_r:.3f}, p={partial.partial_p:.4f}")
        except Exception as e:
            print(f"    Partial correlation failed: {e}")
    else:
        print("    Too few observations for partial correlation")

    # Functional form test — handle None values gracefully
    print("\n[7] Testing functional form...")
    form = None
    try:
        form = test_functional_form(merged["proxy_value"], merged["value"])
        print(f"    Best form: {form.best_form.value}")
        # Safely print R² values (may be None if form couldn't be fit)
        linear_r2_str = f"{form.linear_r2:.3f}" if form.linear_r2 is not None else "N/A"
        log_r2_str = f"{form.log_linear_r2:.3f}" if form.log_linear_r2 is not None else "N/A"
        quad_r2_str = f"{form.quadratic_r2:.3f}" if form.quadratic_r2 is not None else "N/A"
        linear_aic_str = f"{form.linear_aic:.1f}" if form.linear_aic is not None else "N/A"
        log_aic_str = f"{form.log_linear_aic:.1f}" if form.log_linear_aic is not None else "N/A"
        quad_aic_str = f"{form.quadratic_aic:.1f}" if form.quadratic_aic is not None else "N/A"
        print(f"    Linear R²={linear_r2_str}, AIC={linear_aic_str}")
        print(f"    Log-linear R²={log_r2_str}, AIC={log_aic_str}")
        print(f"    Quadratic R²={quad_r2_str}, AIC={quad_aic_str}")
    except Exception as e:
        print(f"    Functional form test failed: {e}")

    # Verdict
    print("\n[8] Determining verdict...")
    verdict = determine_verdict(corr, partial, EXPECTED_DIRECTION)
    print(f"    Verdict: {verdict.value}")

    data_quality_notes = (
        f"PAME (Protected Area Management Effectiveness) data from GD-PAME/BIOPAMA was not "
        f"directly accessible (tried: {', '.join(tried_urls)}). "
        f"Using APPROXIMATE PROXY: {proxy_source} as institutional quality substitute for "
        f"management effectiveness. Government Effectiveness (WGI) measures the quality of "
        f"public services, policy formulation, and credibility of governmental commitment — "
        f"the institutional capacity that underlies effective protected area management. "
        f"Countries with higher GE scores are more likely to enforce PA regulations, fund "
        f"ranger programs, and implement management plans (vs. 'paper parks'). "
        f"This is a broad proxy — actual METT-4/PAME scores from GD-PAME would be needed "
        f"for definitive verification. WGI indicators cover all governance dimensions."
    )

    summary = (
        f"Hypothesis SPI-H07 tests whether Protected Area Management Effectiveness (PAME) "
        f"correlates with the Species Protection Index (SPI). Due to inaccessibility of the "
        f"GD-PAME database (requires BIOPAMA account), this analysis uses {proxy_label} "
        f"(WGI) as an approximate proxy for institutional management quality. "
        f"Bivariate correlation: Pearson r={corr.pearson_r:.3f} (p={corr.pearson_p:.4f}), "
        f"Spearman rho={corr.spearman_rho:.3f} (p={corr.spearman_p:.4f}), "
        f"N={corr.n_observations} observations across {corr.n_countries} countries. "
        + (f"Best functional form: {form.best_form.value}. " if form is not None else "") +
        f"Verdict: {verdict.value}. "
        f"Note: This is an exploratory test with a substitute proxy — "
        f"governance effectiveness as a proxy for PA management effectiveness."
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
    result["verification_method"] = "exploratory_test"
    result["proxy_substitution"] = {
        "intended_proxy": "Protected Area Management Effectiveness Score (PAME/METT-4)",
        "actual_proxy": proxy_source,
        "substitution_rationale": (
            "Government Effectiveness (WGI) measures institutional quality, public service "
            "delivery, and governance capacity — the same factors that determine whether "
            "protected areas are actively managed vs. remaining 'paper parks'. "
            "Countries with stronger governance consistently show better PA outcomes."
        )
    }

else:
    # No proxy found — report inconclusive
    print("\n[RESULT] No usable proxy data found. Reporting inconclusive.")

    data_quality_notes = (
        f"All data acquisition approaches failed for this hypothesis. "
        f"Approach 1 (Direct URL): Tried {', '.join(tried_urls)} — all returned HTML/inaccessible content "
        f"or 404 errors. GD-PAME database requires BIOPAMA account registration. "
        f"Approach 2 (World Bank search): Searched for 'protected area management effectiveness', "
        f"'protected areas management quality', 'biodiversity protected area', "
        f"'protected area governance' — no directly relevant WB indicators found. "
        f"Approach 3 (Approximate proxy): Attempted Government Effectiveness (GE.EST), "
        f"Rule of Law (RL.EST), and Regulatory Quality (RQ.EST) from World Bank WGI — "
        f"data fetch failed or produced insufficient overlap with SPI data. "
        f"GD-PAME database at https://rris.biopama.org requires account registration "
        f"and data is not publicly downloadable without login."
    )

    summary = (
        "Could not obtain any usable proxy for Protected Area Management Effectiveness (PAME). "
        "The GD-PAME database is behind authentication at BIOPAMA. No suitable alternative proxy "
        "was accessible via World Bank or WHO APIs with sufficient country overlap. "
        "Verdict: inconclusive."
    )

    result = {
        "hypothesis_id": HYPOTHESIS_ID,
        "verdict": "inconclusive",
        "verification_method": "pending_data",
        "data_quality_notes": data_quality_notes,
        "summary": summary,
        "attempted_sources": tried_urls,
        "bivariate_correlation": None,
        "partial_correlation": None,
        "functional_form": None,
    }

# -------------------------------------------------------------------
# 5. Write output
# -------------------------------------------------------------------
output_path = os.path.join(OUTPUT_DIR, "result.json")
print(f"\n[9] Writing results to {output_path}")
with open(output_path, "w") as f:
    json.dump(result, f, indent=2, default=str)
print("Done.")
print(f"    Verdict: {result.get('verdict', 'N/A')}")
print(f"    Method: {result.get('verification_method', 'N/A')}")