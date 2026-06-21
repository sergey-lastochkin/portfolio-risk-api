"""Project configuration constants."""

import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
SAMPLE_PORTFOLIO_PATH = DATA_DIR / "sample_portfolio.csv"
SAMPLE_PRICES_PATH = DATA_DIR / "sample_prices.csv"

TRADING_DAYS_PER_YEAR = 252
DEFAULT_VAR_LEVEL = 0.95


def path_endpoints_enabled() -> bool:
    """Return whether server-side CSV paths are safe in this environment."""

    return os.getenv("RENDER", "").strip().lower() != "true"
