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
)
from portfolio_risk_api.scenarios import run_stress_scenarios


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


def _portfolio_notional(portfolio: pd.DataFrame) -> pd.Series:
    indexed = portfolio.set_index("asset")
    return indexed["quantity"].astype(float) * indexed["price"].astype(float)


def _top_positions(
    portfolio: pd.DataFrame,
    weights: pd.Series,
    limit: int = 5,
) -> list[dict[str, Any]]:
    indexed = portfolio.set_index("asset")
    notionals = _portfolio_notional(portfolio)
    rows = []
    for asset, weight in weights.sort_values(ascending=False).head(limit).items():
        rows.append(
            {
                "asset": str(asset),
                "asset_class": str(indexed.loc[asset].get("asset_class", "other")),
                "weight": _clean_value(float(weight)),
                "notional_value": _clean_value(float(notionals.loc[asset])),
            }
        )
    return rows


def _largest_notional_contributors(
    portfolio: pd.DataFrame,
    weights: pd.Series,
    limit: int = 5,
) -> list[dict[str, Any]]:
    notionals = _portfolio_notional(portfolio).sort_values(ascending=False)
    return [
        {
            "asset": str(asset),
            "notional_value": _clean_value(float(notional)),
            "weight": _clean_value(float(weights.loc[asset])),
        }
        for asset, notional in notionals.head(limit).items()
    ]


def _concentration_metrics(weights: pd.Series) -> dict[str, float | None]:
    sorted_weights = weights.sort_values(ascending=False)
    herfindahl = float((weights**2).sum())
    return {
        "top_1_weight": _clean_value(float(sorted_weights.head(1).sum())),
        "top_3_weight": _clean_value(float(sorted_weights.head(3).sum())),
        "effective_number_of_positions": (
            _clean_value(float(1.0 / herfindahl)) if herfindahl > 0 else None
        ),
    }


def _coverage(portfolio: pd.DataFrame, prices: pd.DataFrame) -> dict[str, Any]:
    portfolio_assets = [str(asset) for asset in portfolio["asset"]]
    assets_with_prices = sorted(set(portfolio_assets) & set(prices.columns))
    missing_assets = sorted(set(portfolio_assets) - set(prices.columns))
    return {
        "assets_in_portfolio": len(portfolio_assets),
        "assets_with_price_history": len(assets_with_prices),
        "missing_assets": missing_assets,
    }


def _provenance(
    portfolio: pd.DataFrame,
    prices: pd.DataFrame,
    portfolio_source: str,
    prices_source: str,
) -> dict[str, Any]:
    return {
        "portfolio_source": portfolio_source,
        "prices_source": prices_source,
        "data_window": {
            "start_date": prices.index.min().date().isoformat(),
            "end_date": prices.index.max().date().isoformat(),
            "observations": int(len(prices)),
        },
        "portfolio_columns": [str(column) for column in portfolio.columns],
        "price_assets": [str(column) for column in prices.columns],
    }


def build_risk_report_from_frames(
    portfolio: pd.DataFrame,
    prices: pd.DataFrame,
    var_level: float = 0.95,
    portfolio_source: str = "uploaded portfolio CSV",
    prices_source: str = "uploaded prices CSV",
) -> dict[str, Any]:
    """Build a risk report from validated portfolio and price DataFrames."""

    validate_price_coverage(portfolio, prices)
    weights = asset_weights(portfolio)
    total_value = portfolio_value(portfolio)
    aligned_prices = prices[weights.index]
    returns = portfolio_returns(aligned_prices, weights)
    corr = correlation_matrix(aligned_prices)

    return {
        "portfolio_value": total_value,
        "weights": _series_to_dict(weights),
        "annualized_volatility": _clean_value(annualized_volatility(returns)),
        "max_drawdown": _clean_value(max_drawdown(returns)),
        "var_95": _clean_value(historical_var(returns, var_level)),
        "cvar_95": _clean_value(historical_cvar(returns, var_level)),
        "correlation_matrix": _frame_to_nested_dict(corr),
        "stress_tests": run_stress_scenarios(portfolio),
        "concentration": _concentration_metrics(weights),
        "top_positions": _top_positions(portfolio, weights),
        "largest_notional_contributors": _largest_notional_contributors(portfolio, weights),
        "coverage": _coverage(portfolio, prices),
        "provenance": _provenance(portfolio, prices, portfolio_source, prices_source),
        "observations": int(len(returns)),
        "notes": [
            "Metrics are calculated from the supplied historical price data.",
            "VaR and CVaR are historical estimates and are shown as positive loss numbers.",
            "Stress tests are deterministic scenario shocks for MVP diagnostics.",
        ],
        "limitations": [
            "Sample data is synthetic and should not be presented as live market research.",
            "Historical metrics do not predict future losses.",
            "Scenario outputs are simplified stress diagnostics, not forecasts.",
            "No broker connection, no trading, and no investment advice.",
        ],
    }


def build_risk_report(
    portfolio_path: str,
    prices_path: str,
    var_level: float = 0.95,
) -> dict[str, Any]:
    """Build a risk report from portfolio and price CSV paths."""

    portfolio = load_portfolio_csv(portfolio_path)
    prices = load_prices_csv(prices_path)
    return build_risk_report_from_frames(
        portfolio,
        prices,
        var_level,
        portfolio_source=str(portfolio_path),
        prices_source=str(prices_path),
    )


def build_risk_summary(
    portfolio_path: str,
    prices_path: str,
    var_level: float = 0.95,
) -> dict[str, Any]:
    """Build a smaller risk summary for API consumers."""

    report = build_risk_report(portfolio_path, prices_path, var_level)
    return build_risk_summary_from_report(report)


def build_risk_summary_from_report(report: dict[str, Any]) -> dict[str, Any]:
    """Extract the compact risk summary fields from a richer report."""

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
