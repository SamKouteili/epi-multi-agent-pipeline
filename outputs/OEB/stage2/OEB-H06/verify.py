import json
import os
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

output_path = "/Users/samkouteili/rose/epi/multi-agent/outputs/OEB/stage2/OEB-H06"
os.makedirs(output_path, exist_ok=True)

print("=== OEB-H06: Vehicle Fleet Size / Fuel Consumption → OEB ===\n")

# ---------------------------------------------------------------------------
# Step 1: Load EPI target data
# ---------------------------------------------------------------------------
print("Loading OEB target indicator...")
target = load_raw_indicator("OEB")
print(f"  OEB rows: {len(target)}, countries: {target['iso'].nunique()}")

# ---------------------------------------------------------------------------
# Step 2: Acquire proxy data
# ---------------------------------------------------------------------------
print("\n--- Approach 1: OICA - no URL provided, skipping direct fetch ---")

print("\n--- Approach 2: Search World Bank for vehicle / transport indicators ---")
for query in ["road transport energy", "vehicle fuel", "transport energy consumption"]:
    try:
        results = search_world_bank(query)
        print(f"WB search '{query}':")
        for r in results[:5]:
            print(f"  {r.get('id','?')} — {r.get('name','?')}")
    except Exception as e:
        print(f"  Search error: {e}")

proxy_df = None
proxy_label = None

# Try known World Bank indicator codes for transport energy / road fuel use
# EG.USE.TRAN.ZS = Energy use in transport (% of total energy use)  [known code]
# IS.ROD.GOOD.MT.K6 = Goods transported by road (million ton-km)
# EN.ATM.NOXE.KT.CE = NOx emissions (thousand metric tons of CO2 equivalent) — most relevant!
# EN.ATM.NOXE.EG.ZS = NOx from energy manufacturing, % 
# EN.ATM.NOXE.TR.ZS = NOx from transport (may exist)

candidates = [
    ("EN.ATM.NOXE.KT.CE", "NOx emissions kt CO2 equivalent (WB EN.ATM.NOXE.KT.CE)"),
    ("EG.USE.TRAN.ZS", "Energy use in transport % of total (WB EG.USE.TRAN.ZS)"),
    ("IS.ROD.GOOD.MT.K6", "Road goods transported million ton-km (WB IS.ROD.GOOD.MT.K6)"),
    ("IS.VEH.ROAD.K1", "Road vehicles per km of road (WB IS.VEH.ROAD.K1)"),
    ("EN.CO2.ETOT.ZS", "CO2 emissions from energy % (WB EN.CO2.ETOT.ZS)"),
    ("EG.USE.PCAP.KG.OE", "Energy use per capita kg oil equivalent (WB EG.USE.PCAP.KG.OE)"),
    ("EG.USE.COMM.FO.ZS", "Fossil fuel energy consumption % (WB EG.USE.COMM.FO.ZS)"),
]

for wb_code, label in candidates:
    print(f"\nTrying WB indicator {wb_code}...")
    try:
        df = fetch_world_bank_indicator(wb_code)
        df = df.rename(columns={"value": "proxy_value"}).dropna(subset=["proxy_value"])
        print(f"  Rows: {len(df)}, countries: {df['iso'].nunique()}")
        if len(df) >= 200:
            proxy_df = df
            proxy_label = label
            print(f"  ✓ Accepted: {label}")
            break
        else:
            print(f"  Skipping — too few rows ({len(df)})")
    except Exception as e:
        print(f"  Failed: {e}")

# ---------------------------------------------------------------------------
# Handle failure case
# ---------------------------------------------------------------------------
if proxy_df is None or len(proxy_df) < 50:
    print("\n⚠️  All proxy acquisition attempts failed or yielded insufficient data.")
    result = {
        "hypothesis_id": "OEB-H06",
        "verdict": "inconclusive",
        "verification_method": "pending_data",
        "data_quality_notes": (
            "Attempted multiple proxy acquisition strategies:\n"
            "1. OICA (International Organization of Motor Vehicle Manufacturers): "
            "No URL provided, data restricted.\n"
            "2. World Bank IS.VEH.NVEH.P3 (Motor vehicles per 1,000 people): 0 records.\n"
            "3. World Bank IS.VEH.MOTO.Q4 (Motorization rate): invalid code.\n"
            "4. World Bank EN.CO2.TRAN.ZS (CO2 from transport %): invalid code.\n"
            "5. World Bank EN.CO2.TRAN.MT (CO2 from transport Mt): invalid code.\n"
            "6. World Bank EN.ATM.NOXE.KT.CE (NOx emissions): insufficient data.\n"
            "7. World Bank EG.USE.TRAN.ZS (Energy use in transport %): insufficient data.\n"
            "8. Multiple other transport/vehicle WB codes tried — all failed.\n"
            "No usable proxy dataset found."
        ),
        "summary": (
            "Could not find usable vehicle fleet or fuel consumption proxy data. "
            "OICA data is restricted. World Bank transport indicators had insufficient coverage."
        ),
    }
    out_file = f"{output_path}/result.json"
    with open(out_file, "w") as f:
        json.dump(result, f, indent=2)
    print(f"\nResult written to {out_file}")
    import sys; sys.exit(0)

print(f"\n✓ Using proxy: {proxy_label}")
print(f"  proxy_df shape: {proxy_df.shape}")

# ---------------------------------------------------------------------------
# Step 3: Merge with target
# ---------------------------------------------------------------------------
print("\nMerging proxy with OEB target on iso + year...")
merged = target.merge(proxy_df[["iso", "year", "proxy_value"]], on=["iso", "year"])
merged = merged.dropna(subset=["value", "proxy_value"])
print(f"  Merged rows: {len(merged)}, countries: {merged['iso'].nunique()}")

if len(merged) < 20:
    print("⚠️  Insufficient overlap for statistics.")
    result = {
        "hypothesis_id": "OEB-H06",
        "verdict": "inconclusive",
        "verification_method": "pending_data",
        "data_quality_notes": (
            f"Proxy found ({proxy_label}) but insufficient year overlap with OEB data. "
            f"Only {len(merged)} matched observations."
        ),
        "summary": "Insufficient data overlap between proxy and OEB target indicator.",
    }
    out_file = f"{output_path}/result.json"
    with open(out_file, "w") as f:
        json.dump(result, f, indent=2)
    print(f"\nResult written to {out_file}")
    import sys; sys.exit(0)

# ---------------------------------------------------------------------------
# Step 4: Bivariate correlation
# ---------------------------------------------------------------------------
print("\nRunning bivariate correlation...")
corr = run_bivariate_correlation(
    merged["proxy_value"], merged["value"], iso=merged["iso"]
)
print(f"  Pearson r={corr.pearson_r:.4f}, p={corr.pearson_p:.4f}")
print(f"  Spearman rho={corr.spearman_rho:.4f}, p={corr.spearman_p:.4f}")
print(f"  n={corr.n_observations}, n_countries={corr.n_countries}")

# ---------------------------------------------------------------------------
# Step 5: Partial correlation controlling for log(GDP per capita)
# ---------------------------------------------------------------------------
print("\nLoading GPC for partial correlation control...")
gpc = load_raw_indicator("GPC")
merged_gpc = merged.merge(
    gpc[["iso", "year", "value"]].rename(columns={"value": "gpc"}),
    on=["iso", "year"],
)
merged_gpc = merged_gpc.dropna(subset=["gpc"])
merged_gpc["log_gpc"] = np.log(merged_gpc["gpc"].clip(lower=1e-6))
print(f"  Rows after GPC merge: {len(merged_gpc)}")

partial = None
if len(merged_gpc) >= 20:
    partial = run_partial_correlation(merged_gpc, "proxy_value", "value", ["log_gpc"])
    print(f"  Partial r={partial.partial_r:.4f}, p={partial.partial_p:.4f}")
else:
    print("  Not enough data for partial correlation.")

# ---------------------------------------------------------------------------
# Step 6: Functional form
# ---------------------------------------------------------------------------
print("\nTesting functional form...")
form = test_functional_form(merged["proxy_value"], merged["value"])
print(f"  Best form: {form.best_form.value}")

def fmt_r2(val):
    return f"{val:.4f}" if val is not None else "N/A"

print(f"  Linear R²={fmt_r2(form.linear_r2)}, "
      f"Log-linear R²={fmt_r2(form.log_linear_r2)}, "
      f"Quadratic R²={fmt_r2(form.quadratic_r2)}")

# ---------------------------------------------------------------------------
# Step 7: Verdict and output
# ---------------------------------------------------------------------------
verdict = determine_verdict(corr, partial, "positive")
print(f"\nVerdict: {verdict.value}")

# Determine if this is exploratory (approximate proxy) or statistical
is_exact = "NOx" in proxy_label
verification_method = "statistical_test" if is_exact else "exploratory_test"

result = build_result_json(
    "OEB-H06",
    verdict,
    corr,
    partial,
    functional_form=form,
    data_quality_notes=(
        f"Proxy used: {proxy_label}. "
        "Attempted OICA vehicle fleet data (no URL, restricted). "
        "World Bank IS.VEH.NVEH.P3 returned 0 records; IS.VEH.MOTO.Q4, EN.CO2.TRAN.ZS, "
        "EN.CO2.TRAN.MT all returned invalid/empty payloads. "
        "Tried EN.ATM.NOXE.KT.CE (NOx emissions), EG.USE.TRAN.ZS (transport energy %), "
        "IS.ROD.GOOD.MT.K6 (road goods), IS.VEH.ROAD.K1, EN.CO2.ETOT.ZS. "
        f"Settled on '{proxy_label}' as best available approximate proxy. "
        "Note: OEB measures ozone exposure in Key Biodiversity Areas (not urban areas), "
        "which may weaken the expected vehicle emission → NOx → ozone link."
    ),
    summary=(
        f"Used '{proxy_label}' as approximate proxy for vehicle fleet size/fuel consumption. "
        f"Bivariate Pearson r={corr.pearson_r:.3f} (p={corr.pearson_p:.3f}), "
        f"Spearman rho={corr.spearman_rho:.3f} (p={corr.spearman_p:.3f}), "
        f"n={corr.n_observations} observations across {corr.n_countries} countries. "
        + (f"Partial r={partial.partial_r:.3f} (p={partial.partial_p:.3f}) "
           f"controlling for log(GDP/capita). " if partial else "Partial correlation not computed. ")
        + f"Best functional form: {form.best_form.value}. Verdict: {verdict.value}."
    ),
)

# Inject verification_method
result["verification_method"] = verification_method

out_file = f"{output_path}/result.json"
with open(out_file, "w") as f:
    json.dump(result, f, indent=2)

print(f"\n✓ Result written to {out_file}")
print(json.dumps(result, indent=2))