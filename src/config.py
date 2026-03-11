"""Paths, API keys, constants, and configuration for the EPI proxy discovery pipeline."""

from pathlib import Path
import os

from dotenv import load_dotenv

load_dotenv()

# ── Paths ──────────────────────────────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).resolve().parent.parent
EPI_DATA_DIR = PROJECT_ROOT / "docs" / "EPI2024_Work"
RAW_DIR = EPI_DATA_DIR / "Raw"
INPUTS_DIR = EPI_DATA_DIR / "Inputs"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"

MASTER_VARIABLE_LIST = INPUTS_DIR / "master_variable_list.csv"
MASTER_FILE = INPUTS_DIR / "MasterFile.csv"
COUNTRY_DICTIONARY = INPUTS_DIR / "cdictionary_expanded.csv"
ATTRIBUTES_FILE = INPUTS_DIR / "Attributes.csv"

# ── API Keys ───────────────────────────────────────────────────────────────────
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")

# ── Model Names ────────────────────────────────────────────────────────────────
GEMINI_DEEP_RESEARCH_AGENT = "deep-research-pro-preview-12-2025"
CLAUDE_PARSING_MODEL = "claude-sonnet-4-20250514"
CLAUDE_VERIFICATION_MODEL = "claude-sonnet-4-6"
CLAUDE_VALIDATION_MODEL = "claude-haiku-4-5-20251001"
VALIDATION_MAX_TOKENS = 2048

# ── EPI Data Constants ─────────────────────────────────────────────────────────
MISSING_SENTINELS = {-9999, -8888, -7777}
CONTROL_VARIABLE_TLAS = ["GPC", "POP", "URB"]

# ── Verdict Thresholds ─────────────────────────────────────────────────────────
VERDICT_R_THRESHOLD = 0.3          # |r| must exceed this for "confirmed"
VERDICT_P_THRESHOLD = 0.05         # p must be below this for significance
VERDICT_P_BORDERLINE = 0.10        # p between 0.05-0.10 = "inconclusive"
VERDICT_MIN_N = 20                 # minimum observations for any verdict
PARTIAL_CORR_MIN_N = 30            # minimum observations for partial correlation
VERDICT_R_STRONG = 0.5             # |r| threshold for confirmed without partial corr
VERDICT_P_STRICT = 0.01            # p threshold for confirmed without partial corr

# ── Pipeline Defaults ──────────────────────────────────────────────────────────
MAX_HYPOTHESES = 10
DEEP_RESEARCH_POLL_INTERVAL = 10  # seconds between status checks
DEEP_RESEARCH_MAX_WAIT = 3600     # max seconds to wait (60 min)
API_RETRY_ATTEMPTS = 3
API_RETRY_BACKOFF = 2.0
