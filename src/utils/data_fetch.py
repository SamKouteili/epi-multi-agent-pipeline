"""Data fetching utilities: World Bank API, WHO GHO API, and local indicator discovery.

Provides reusable wrappers so Stage 2 verification agents don't need to write
API boilerplate from scratch. All fetch functions return a standardized
long-format DataFrame with columns (iso, year, value) that merges directly
with load_raw_indicator() output on (iso, year).
"""

import logging
from urllib.parse import quote

import pandas as pd
import requests

from src.config import MASTER_FILE, MASTER_VARIABLE_LIST

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Local control variables — already on disk as raw CSVs.
# Agents should use load_raw_indicator(TLA) for these, NOT re-download them.
# ---------------------------------------------------------------------------
LOCAL_CONTROLS: dict[str, str] = {
    "GPC": "GDP per capita, PPP (constant 2017 intl $)",
    "HDI": "Human Development Index (0-1)",
    "POP": "Total population",
    "URB": "Urban population (% of total)",
}

_WB_BASE = "https://api.worldbank.org/v2"
_WHO_BASE = "https://ghoapi.azureedge.net/api"
_REQUEST_TIMEOUT = 60

_epi_iso_cache: set[str] | None = None


def _get_epi_iso_set() -> set[str]:
    """Return the set of ISO3 codes from MasterFile.csv (cached after first call).

    If the file is missing or unreadable, returns an empty set so that
    downstream filtering degrades gracefully (no ISOs are excluded).
    """
    global _epi_iso_cache
    if _epi_iso_cache is not None:
        return _epi_iso_cache
    try:
        df = pd.read_csv(MASTER_FILE)
        _epi_iso_cache = set(df["iso"].dropna().astype(str).str.strip())
    except Exception as exc:
        logger.warning("Could not read MasterFile.csv for ISO filtering: %s", exc)
        _epi_iso_cache = set()
    return _epi_iso_cache


# ---------------------------------------------------------------------------
# World Bank
# ---------------------------------------------------------------------------

def fetch_world_bank_indicator(
    indicator_code: str,
    year_range: tuple[int, int] = (1990, 2024),
) -> pd.DataFrame:
    """Fetch any World Bank indicator by code.

    Returns a DataFrame with columns ``iso``, ``year``, ``value``.
    Handles pagination, null filtering, and ISO3 validation.
    Returns an empty DataFrame on failure (with a logged warning).

    Parameters
    ----------
    indicator_code : str
        World Bank indicator code, e.g. ``"SH.H2O.BASW.ZS"`` or ``"NY.GDP.PCAP.PP.KD"``.
    year_range : tuple[int, int]
        Inclusive (start, end) year range.
    """
    start, end = year_range
    url = (
        f"{_WB_BASE}/country/all/indicator/{indicator_code}"
        f"?format=json&per_page=20000&date={start}:{end}"
    )

    try:
        resp = requests.get(url, timeout=_REQUEST_TIMEOUT)
        resp.raise_for_status()
        payload = resp.json()
    except (requests.RequestException, ValueError) as exc:
        logger.warning("World Bank fetch failed for %s: %s", indicator_code, exc)
        return pd.DataFrame(columns=["iso", "year", "value"])

    # The WB JSON API returns a two-element list: [metadata, records].
    if not isinstance(payload, list) or len(payload) < 2 or payload[1] is None:
        logger.warning(
            "World Bank returned unexpected payload for %s (possibly invalid code)",
            indicator_code,
        )
        return pd.DataFrame(columns=["iso", "year", "value"])

    epi_isos = _get_epi_iso_set()

    records: list[dict] = []
    for item in payload[1]:
        iso = item.get("countryiso3code", "")
        val = item.get("value")
        date = item.get("date", "")
        # Skip nulls, aggregates (empty ISO or wrong length), bad years
        if val is None or len(iso) != 3 or not date.isdigit():
            continue
        # Filter out WB region/income aggregate codes (WLD, SSA, HIC, etc.)
        if epi_isos and iso not in epi_isos:
            continue
        records.append({"iso": iso, "year": int(date), "value": float(val)})

    if not records:
        logger.warning("World Bank returned 0 valid records for %s", indicator_code)

    return pd.DataFrame(records, columns=["iso", "year", "value"])


def search_world_bank(query: str, max_results: int = 10) -> list[dict]:
    """Search the World Bank indicator catalog by keyword.

    Returns a list of ``{"id", "name", "source"}`` dicts (up to *max_results*).
    Useful when the agent doesn't know the exact indicator code.
    """
    url = (
        f"{_WB_BASE}/indicator"
        f"?format=json&per_page={max_results}&qterm={quote(query)}"
    )

    try:
        resp = requests.get(url, timeout=_REQUEST_TIMEOUT)
        resp.raise_for_status()
        payload = resp.json()
    except (requests.RequestException, ValueError) as exc:
        logger.warning("World Bank search failed for %r: %s", query, exc)
        return []

    if not isinstance(payload, list) or len(payload) < 2 or payload[1] is None:
        return []

    results: list[dict] = []
    for item in payload[1]:
        results.append({
            "id": item.get("id", ""),
            "name": item.get("name", ""),
            "source": item.get("source", {}).get("value", ""),
        })
    return results


# ---------------------------------------------------------------------------
# WHO Global Health Observatory
# ---------------------------------------------------------------------------

def _dedup_who_gho(df: pd.DataFrame, indicator_code: str) -> pd.DataFrame:
    """Remove WHO GHO sub-dimension duplicates (sex/area breakdowns).

    Many GHO indicators return multiple rows per (iso, year) — e.g. one each
    for male, female, and both-sexes. We keep only the aggregate row:

    1. If all ``Dim1`` values are None → no breakdowns, pass through unchanged.
    2. If rows with ``_BTSX`` or ``_TOTL`` suffix exist → keep only those.
    3. Otherwise (unknown Dim1 pattern) → log a warning and pass through
       unchanged rather than silently picking an arbitrary breakdown.
    """
    if "Dim1" not in df.columns or df.empty:
        return df

    dim1_values = df["Dim1"].unique()

    # Case 1: all None — no sub-dimensions at all
    if len(dim1_values) == 1 and pd.isna(dim1_values[0]):
        return df.drop(columns=["Dim1"])

    # Case 2: aggregate markers present — keep only those
    aggregate_mask = df["Dim1"].str.endswith("_BTSX", na=False) | df["Dim1"].str.endswith("_TOTL", na=False)
    if aggregate_mask.any():
        before = len(df)
        df = df[aggregate_mask].copy()
        logger.info(
            "WHO GHO %s: deduped %d → %d rows (kept _BTSX/_TOTL aggregates)",
            indicator_code, before, len(df),
        )
        return df.drop(columns=["Dim1"])

    # Case 3: unknown Dim1 pattern — warn and pass through
    non_null = [v for v in dim1_values if pd.notna(v)]
    logger.warning(
        "WHO GHO %s: unknown Dim1 values %s — skipping dedup. "
        "Data may contain duplicate (iso, year) rows.",
        indicator_code, non_null[:5],
    )
    return df.drop(columns=["Dim1"])


def fetch_who_gho_indicator(indicator_code: str) -> pd.DataFrame:
    """Fetch any WHO GHO indicator by code.

    Returns a DataFrame with columns ``iso``, ``year``, ``value``.
    Uses the GHO OData API at ``https://ghoapi.azureedge.net/api/{code}``.
    Deduplicates sub-dimension breakdowns (sex, area) to avoid row inflation.
    Returns an empty DataFrame on failure.

    Parameters
    ----------
    indicator_code : str
        WHO GHO indicator code, e.g. ``"WHOSIS_000001"`` or ``"WHS3_41"``.
    """
    url = f"{_WHO_BASE}/{indicator_code}"

    try:
        resp = requests.get(url, timeout=_REQUEST_TIMEOUT)
        resp.raise_for_status()
        payload = resp.json()
    except (requests.RequestException, ValueError) as exc:
        logger.warning("WHO GHO fetch failed for %s: %s", indicator_code, exc)
        return pd.DataFrame(columns=["iso", "year", "value"])

    items = payload.get("value", [])
    records: list[dict] = []
    for item in items:
        iso = item.get("SpatialDim", "")
        year = item.get("TimeDim")
        val = item.get("NumericValue")
        dim1 = item.get("Dim1")
        if val is None or len(iso) != 3 or year is None:
            continue
        try:
            records.append({
                "iso": iso, "year": int(year), "value": float(val), "Dim1": dim1,
            })
        except (ValueError, TypeError):
            continue

    if not records:
        logger.warning("WHO GHO returned 0 valid records for %s", indicator_code)
        return pd.DataFrame(columns=["iso", "year", "value"])

    df = pd.DataFrame(records)
    df = _dedup_who_gho(df, indicator_code)
    return df[["iso", "year", "value"]]


# ---------------------------------------------------------------------------
# Local indicator discovery
# ---------------------------------------------------------------------------

def list_local_indicators() -> list[dict]:
    """List all TLAs available as local raw CSVs in the EPI data directory.

    Reads ``master_variable_list.csv`` and filters to rows where
    ``RawFileExists == "yes"``. Returns a list of dicts with keys
    ``tla``, ``description``, ``type``, ``source``.

    Agents can call this to discover what's already on disk before
    attempting to download data from an external API.
    """
    try:
        df = pd.read_csv(MASTER_VARIABLE_LIST)
    except Exception as exc:
        logger.warning("Could not read master_variable_list.csv: %s", exc)
        return []

    available = df[df["RawFileExists"].str.strip().str.lower() == "yes"]

    results: list[dict] = []
    for _, row in available.iterrows():
        results.append({
            "tla": row.get("Abbreviation", ""),
            "description": row.get("Description", ""),
            "type": row.get("Type", ""),
            "source": row.get("Source", ""),
        })
    return results
