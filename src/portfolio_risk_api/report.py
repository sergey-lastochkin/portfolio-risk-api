"""Risk report assembly."""

import math
from typing import Any

import pandas as pd

from portfolio_risk_api.data_loader import (
    load_portfolio_csv,
    load_prices_csv,
    validate_price_coverage,
)
from portfolio_risk_api.risk_metrics import (
    annualized_volatility,
    asset_weights,
    correlation_matrix,
    historical_cvar,
    historical_var,
    max_drawdown,
    portfolio_returns,
    portfolio_value,
    simple_stress_tests,
)


def _clean_value(value: Any) -> Any:
    if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
        return None
    return value


def _series_to_dict(series: pd.Series) -> dict[str, float | None]:
    return {str(index): _clean_value(float(value)) for index, value in series.items()}


def _frame_to_nested_dict(frame: pd.DataFrame) -> dict[str, dict[str, float | None]]:
    return {
        str(index): {str(column): _clean_value(float(value)) for column, value in row.items()}
        for index, row in frame.iterrows()
    }


def build_risk_report(
    portfolio_path: str,
    prices_path: str,
    var_level: float = 0.95,
) -> dict[str, Any]:
    """Build a compact risk report from portfolio and price CSV paths."""

    portfolio = load_portfolio_csv(portfolio_path)
    prices = load_prices_csv(prices_path)
    validate_price_coverage(portfolio, prices)

    weights = asset_weights(portfolio)
    total_value = portfolio_value(portfolio)
    returns = portfolio_returns(prices, weights)
    corr = correlation_matrix(prices[weights.index])

    return {
        "portfolio_value": total_value,
        "weights": _series_to_dict(weights),
        "annualized_volatility": _clean_value(annualized_volatility(returns)),
        "max_drawdown": _clean_value(max_drawdown(returns)),
        "var_95": _clean_value(historical_var(returns, var_level)),
        "cvar_95": _clean_value(historical_cvar(returns, var_level)),
        "correlation_matrix": _frame_to_nested_dict(corr),
        "stress_tests": simple_stress_tests(weights, total_value),
        "observations": int(len(returns)),
        "notes": [
            "Metrics are calculated from the supplied historical price data.",
            "VaR and CVaR are historical estimates and are shown as positive loss numbers.",
            "Stress tests are simplified uniform shocks for MVP diagnostics.",
        ],
        "limitations": [
            "Sample data is synthetic and should not be presented as live market research.",
            "Historical metrics do not predict future losses.",
            "No broker connection, no trading, and no investment advice.",
        ],
    }


def build_risk_summary(
    portfolio_path: str,
    prices_path: str,
    var_level: float = 0.95,
) -> dict[str, Any]:
    """Build a smaller risk summary for API consumers."""

    report = build_risk_report(portfolio_path, prices_path, var_level)
    return {
        key: report[key]
        for key in [
            "portfolio_value",
            "weights",
            "annualized_volatility",
            "max_drawdown",
            "var_95",
            "cvar_95",
            "observations",
            "stress_tests",
            "limitations",
        ]
    }
