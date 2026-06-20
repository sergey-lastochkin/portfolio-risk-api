"""CSV loading and validation utilities."""

from pathlib import Path

import pandas as pd

REQUIRED_PORTFOLIO_COLUMNS = {"asset", "quantity", "price"}
REQUIRED_PRICE_COLUMNS = {"date"}
MIN_PRICE_OBSERVATIONS = 3


class DataValidationError(ValueError):
    """Raised when input CSV data does not match the expected schema."""


def _resolve_path(path: str | Path) -> Path:
    resolved = Path(path).expanduser()
    if not resolved.is_absolute():
        resolved = Path.cwd() / resolved
    return resolved


def load_portfolio_csv(path: str | Path) -> pd.DataFrame:
    """Load and validate a portfolio CSV file."""

    resolved = _resolve_path(path)
    if not resolved.exists():
        raise DataValidationError(f"Portfolio file not found: {resolved}")

    df = pd.read_csv(resolved)
    missing = REQUIRED_PORTFOLIO_COLUMNS - set(df.columns)
    if missing:
        raise DataValidationError(f"Portfolio CSV missing columns: {sorted(missing)}")

    result = df.copy()
    result["asset"] = result["asset"].astype(str).str.strip()
    result["quantity"] = pd.to_numeric(result["quantity"], errors="coerce")
    result["price"] = pd.to_numeric(result["price"], errors="coerce")

    if result["asset"].eq("").any():
        raise DataValidationError("Portfolio CSV contains empty asset names.")
    if result[["quantity", "price"]].isna().any().any():
        raise DataValidationError("Portfolio CSV contains non-numeric quantity or price values.")
    if (result["price"] <= 0).any():
        raise DataValidationError("Portfolio CSV contains non-positive prices.")

    return result


def load_prices_csv(path: str | Path) -> pd.DataFrame:
    """Load and validate a price CSV file with a date column and asset price columns."""

    resolved = _resolve_path(path)
    if not resolved.exists():
        raise DataValidationError(f"Prices file not found: {resolved}")

    df = pd.read_csv(resolved)
    missing = REQUIRED_PRICE_COLUMNS - set(df.columns)
    if missing:
        raise DataValidationError(f"Prices CSV missing columns: {sorted(missing)}")
    if len(df.columns) < 2:
        raise DataValidationError("Prices CSV must contain at least one asset price column.")

    result = df.copy()
    result["date"] = pd.to_datetime(result["date"], errors="coerce")
    if result["date"].isna().any():
        raise DataValidationError("Prices CSV contains invalid dates.")
    if result["date"].duplicated().any():
        raise DataValidationError("Prices CSV contains duplicate dates.")

    asset_columns = [column for column in result.columns if column != "date"]
    for column in asset_columns:
        result[column] = pd.to_numeric(result[column], errors="coerce")

    if result[asset_columns].isna().any().any():
        raise DataValidationError("Prices CSV contains non-numeric or missing prices.")
    if (result[asset_columns] <= 0).any().any():
        raise DataValidationError("Prices CSV contains non-positive prices.")

    result = result.sort_values("date").set_index("date")
    if len(result) < MIN_PRICE_OBSERVATIONS:
        raise DataValidationError(
            f"Prices CSV contains insufficient price history: "
            f"at least {MIN_PRICE_OBSERVATIONS} rows are required."
        )
    return result


def validate_price_coverage(portfolio: pd.DataFrame, prices: pd.DataFrame) -> None:
    """Ensure that the price table contains all portfolio assets."""

    missing_assets = sorted(set(portfolio["asset"]) - set(prices.columns))
    if missing_assets:
        raise DataValidationError(f"Prices CSV missing portfolio assets: {missing_assets}")
