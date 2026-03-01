"""EPI data loading utilities: CSV loading, sentinel handling, long-format conversion."""

import re

import pandas as pd

from src.config import RAW_DIR, MASTER_VARIABLE_LIST, MISSING_SENTINELS


def load_raw_indicator(tla: str) -> pd.DataFrame:
    """Load a raw EPI indicator CSV and return it in long format.

    Returns DataFrame with columns: code, iso, country, year, value
    Sentinels (-9999, -8888, -7777) are replaced with NaN.
    """
    path = RAW_DIR / f"{tla}_raw.csv"
    if not path.exists():
        raise FileNotFoundError(f"Raw data file not found: {path}")

    df = pd.read_csv(path)

    # Identify year columns matching pattern {TLA}.raw.{YYYY}
    year_cols = [c for c in df.columns if re.match(rf"{tla}\.raw\.\d{{4}}", c)]
    id_cols = ["code", "iso", "country"]

    # Melt to long format
    long = df.melt(id_vars=id_cols, value_vars=year_cols, var_name="year_col", value_name="value")

    # Extract year from column name
    long["year"] = long["year_col"].str.extract(r"(\d{4})").astype(int)
    long = long.drop(columns=["year_col"])

    # Replace sentinels with NaN
    long.loc[long["value"].isin(MISSING_SENTINELS), "value"] = pd.NA
    long["value"] = pd.to_numeric(long["value"], errors="coerce")

    # Drop rows with missing values
    long = long.dropna(subset=["value"]).reset_index(drop=True)

    return long[["code", "iso", "country", "year", "value"]]


def load_variable_metadata(tla: str) -> dict:
    """Look up an indicator's metadata from master_variable_list.csv."""
    df = pd.read_csv(MASTER_VARIABLE_LIST)
    row = df[df["Abbreviation"] == tla]
    if row.empty:
        raise ValueError(f"Indicator '{tla}' not found in master variable list")
    return row.iloc[0].to_dict()


def get_available_indicators() -> list[dict]:
    """Return metadata for all indicators in the master variable list."""
    df = pd.read_csv(MASTER_VARIABLE_LIST)
    indicators = df[df["Type"] == "Indicator"]
    return indicators.to_dict("records")
