"""Country name normalization and dataframe alignment utilities."""

from __future__ import annotations

from functools import lru_cache
from typing import Optional

import pandas as pd
from thefuzz import fuzz

from src.config import COUNTRY_DICTIONARY, MASTER_FILE


@lru_cache(maxsize=1)
def build_country_lookup() -> dict[str, tuple[int, str, str]]:
    """Build a lookup dict mapping country name variants → (code, iso, country).

    Combines cdictionary_expanded.csv (wrong→right mappings) and MasterFile.csv.
    """
    lookup: dict[str, tuple[int, str, str]] = {}

    # Load canonical country list
    master = pd.read_csv(MASTER_FILE)
    for _, row in master.iterrows():
        key = str(row["country"]).strip().lower()
        val = (int(row["code"]), str(row["iso"]).strip(), str(row["country"]).strip())
        lookup[key] = val
        # Also index by ISO code
        lookup[str(row["iso"]).strip().lower()] = val

    # Load country dictionary (wrong → right mappings)
    cdict = pd.read_csv(COUNTRY_DICTIONARY, encoding="latin-1")
    for _, row in cdict.iterrows():
        if pd.isna(row["code"]) or pd.isna(row["iso"]):
            continue
        wrong = str(row["wrong"]).strip().lower()
        code = int(row["code"])
        iso = str(row["iso"]).strip()
        right = str(row["right"]).strip()
        lookup[wrong] = (code, iso, right)

    return lookup


def normalize_country(name: str, fuzzy_threshold: int = 85) -> Optional[tuple[int, str, str]]:
    """Normalize a country name to (code, iso, country).

    First tries exact match (case-insensitive), then fuzzy matching.
    Returns None if no match found above the threshold.
    """
    lookup = build_country_lookup()
    key = name.strip().lower()

    # Exact match
    if key in lookup:
        return lookup[key]

    # Fuzzy match
    best_score = 0
    best_match = None
    for candidate in lookup:
        score = fuzz.ratio(key, candidate)
        if score > best_score:
            best_score = score
            best_match = candidate

    if best_match and best_score >= fuzzy_threshold:
        return lookup[best_match]

    return None


def align_dataframes(
    epi_df: pd.DataFrame,
    proxy_df: pd.DataFrame,
    proxy_country_col: str = "country",
    proxy_year_col: str = "year",
    proxy_value_col: str = "value",
) -> pd.DataFrame:
    """Align an EPI indicator dataframe with a proxy dataframe on ISO code + year.

    The EPI dataframe should already be in long format from load_raw_indicator().
    The proxy dataframe needs a country column (name or ISO) and a year column.

    Returns a merged DataFrame with columns:
        code, iso, country, year, epi_value, proxy_value
    """
    # Normalize proxy country names to ISO codes
    normalized = []
    for _, row in proxy_df.iterrows():
        result = normalize_country(str(row[proxy_country_col]))
        if result:
            code, iso, country = result
            normalized.append({
                "iso": iso,
                "year": int(row[proxy_year_col]),
                "proxy_value": row[proxy_value_col],
            })

    if not normalized:
        return pd.DataFrame(columns=["code", "iso", "country", "year", "epi_value", "proxy_value"])

    proxy_norm = pd.DataFrame(normalized)

    # If there are duplicate iso+year entries in proxy, take the mean
    proxy_norm = proxy_norm.groupby(["iso", "year"], as_index=False)["proxy_value"].mean()

    # Rename EPI value column for clarity
    epi_renamed = epi_df.rename(columns={"value": "epi_value"})

    # Merge on ISO + year
    merged = epi_renamed.merge(proxy_norm, on=["iso", "year"], how="inner")

    return merged
