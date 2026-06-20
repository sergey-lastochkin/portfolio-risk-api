import pytest

from portfolio_risk_api.data_loader import (
    DataValidationError,
    load_portfolio_csv,
    load_prices_csv,
    validate_price_coverage,
)


def test_load_sample_files():
    portfolio = load_portfolio_csv("data/sample_portfolio.csv")
    prices = load_prices_csv("data/sample_prices.csv")
    validate_price_coverage(portfolio, prices)

    assert set(portfolio.columns) == {"asset", "quantity", "price"}
    assert "AAPL" in prices.columns
    assert len(prices) > 10


def test_missing_portfolio_columns(tmp_path):
    path = tmp_path / "bad_portfolio.csv"
    path.write_text("asset,quantity\nAAPL,10\n", encoding="utf-8")

    with pytest.raises(DataValidationError):
        load_portfolio_csv(path)


def test_missing_price_columns(tmp_path):
    path = tmp_path / "bad_prices.csv"
    path.write_text("AAPL,MSFT\n100,200\n", encoding="utf-8")

    with pytest.raises(DataValidationError):
        load_prices_csv(path)


def test_nan_prices_are_rejected(tmp_path):
    path = tmp_path / "nan_prices.csv"
    path.write_text(
        "date,AAPL\n2026-01-01,100\n2026-01-02,\n2026-01-03,101\n",
        encoding="utf-8",
    )

    with pytest.raises(DataValidationError, match="missing prices"):
        load_prices_csv(path)


def test_zero_and_negative_prices_are_rejected(tmp_path):
    path = tmp_path / "bad_prices.csv"
    path.write_text(
        "date,AAPL\n2026-01-01,100\n2026-01-02,0\n2026-01-03,-1\n",
        encoding="utf-8",
    )

    with pytest.raises(DataValidationError, match="non-positive prices"):
        load_prices_csv(path)


def test_insufficient_price_history_is_rejected(tmp_path):
    path = tmp_path / "short_prices.csv"
    path.write_text("date,AAPL\n2026-01-01,100\n2026-01-02,101\n", encoding="utf-8")

    with pytest.raises(DataValidationError, match="insufficient price history"):
        load_prices_csv(path)


def test_unknown_asset_in_prices_raises_clear_error(tmp_path):
    portfolio_path = tmp_path / "portfolio.csv"
    prices_path = tmp_path / "prices.csv"
    portfolio_path.write_text("asset,quantity,price\nAAPL,1,100\nMSFT,1,200\n", encoding="utf-8")
    prices_path.write_text(
        "date,AAPL\n2026-01-01,100\n2026-01-02,101\n2026-01-03,102\n",
        encoding="utf-8",
    )

    portfolio = load_portfolio_csv(portfolio_path)
    prices = load_prices_csv(prices_path)

    with pytest.raises(DataValidationError, match="missing portfolio assets"):
        validate_price_coverage(portfolio, prices)
