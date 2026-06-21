import numpy as np
import pandas as pd

from portfolio_risk_api.data_loader import load_portfolio_csv, load_prices_csv
from portfolio_risk_api.risk_metrics import (
    annualized_volatility,
    asset_weights,
    historical_cvar,
    historical_var,
    max_drawdown,
    portfolio_returns,
    portfolio_value,
    simple_stress_tests,
)
from portfolio_risk_api.scenarios import asset_class_map, run_stress_scenarios


def test_weights_sum_to_one():
    portfolio = load_portfolio_csv("data/sample_portfolio.csv")
    weights = asset_weights(portfolio)

    assert np.isclose(weights.sum(), 1.0)
    assert portfolio_value(portfolio) > 0


def test_risk_metrics_are_finite_or_non_negative():
    portfolio = load_portfolio_csv("data/sample_portfolio.csv")
    prices = load_prices_csv("data/sample_prices.csv")
    returns = portfolio_returns(prices, asset_weights(portfolio))

    assert annualized_volatility(returns) >= 0
    assert max_drawdown(returns) <= 0
    assert historical_var(returns) >= 0
    assert historical_cvar(returns) >= 0


def test_constant_price_series_gives_zero_returns_and_near_zero_volatility():
    prices = pd.DataFrame(
        {"AAPL": [100.0, 100.0, 100.0, 100.0]},
        index=pd.date_range("2026-01-01", periods=4),
    )
    weights = pd.Series({"AAPL": 1.0})

    returns = portfolio_returns(prices, weights)

    assert np.allclose(returns.to_numpy(), 0.0)
    assert np.isclose(annualized_volatility(returns), 0.0)


def test_single_asset_portfolio_weight_sums_to_one():
    portfolio = pd.DataFrame({"asset": ["AAPL"], "quantity": [2.0], "price": [100.0]})

    weights = asset_weights(portfolio)

    assert np.isclose(weights.sum(), 1.0)
    assert np.isclose(weights["AAPL"], 1.0)


def test_two_asset_portfolio_weight_sums_to_one():
    portfolio = pd.DataFrame(
        {"asset": ["AAPL", "MSFT"], "quantity": [1.0, 1.0], "price": [100.0, 300.0]}
    )

    weights = asset_weights(portfolio)

    assert np.isclose(weights.sum(), 1.0)
    assert np.isclose(weights["AAPL"], 0.25)
    assert np.isclose(weights["MSFT"], 0.75)


def test_falling_price_series_produces_negative_drawdown():
    prices = pd.DataFrame(
        {"AAPL": [100.0, 95.0, 90.0, 85.0]},
        index=pd.date_range("2026-01-01", periods=4),
    )
    weights = pd.Series({"AAPL": 1.0})

    returns = portfolio_returns(prices, weights)

    assert max_drawdown(returns) < 0


def test_var_and_cvar_are_positive_loss_numbers():
    returns = pd.Series([0.01, -0.02, 0.005, -0.04, 0.003])

    var = historical_var(returns, level=0.8)
    cvar = historical_cvar(returns, level=0.8)

    assert var >= 0
    assert cvar >= 0
    assert cvar >= var


def test_stress_test_output_has_stable_keys():
    weights = pd.Series({"AAPL": 0.5, "MSFT": 0.5})
    output = simple_stress_tests(weights, portfolio_total=1000.0)

    assert output
    assert set(output[0]) == {"scenario", "shock", "portfolio_pnl", "portfolio_pnl_pct"}


def test_asset_class_map_uses_explicit_and_inferred_classes():
    portfolio = pd.DataFrame(
        {
            "asset": ["AAPL", "BTC", "EURUSD"],
            "quantity": [1.0, 1.0, 1.0],
            "price": [100.0, 60000.0, 1.1],
        }
    )

    classes = asset_class_map(portfolio)

    assert classes == {"AAPL": "equity", "BTC": "crypto", "EURUSD": "fx"}


def test_scenario_engine_returns_stable_keys_and_negative_pnl():
    portfolio = pd.DataFrame(
        {
            "asset": ["AAPL", "BTC", "EURUSD"],
            "quantity": [1.0, 0.1, 1000.0],
            "price": [100.0, 60000.0, 1.1],
            "asset_class": ["equity", "crypto", "fx"],
        }
    )

    output = run_stress_scenarios(portfolio)
    broad_down = next(item for item in output if item["scenario_name"] == "all_assets_down_10pct")

    assert set(broad_down) == {
        "scenario_name",
        "portfolio_pnl",
        "portfolio_pnl_pct",
        "per_asset_impact",
    }
    assert broad_down["portfolio_pnl"] < 0
    assert broad_down["portfolio_pnl_pct"] < 0
