"""Core portfolio risk calculations."""

import numpy as np
import pandas as pd

from portfolio_risk_api.config import TRADING_DAYS_PER_YEAR


def portfolio_value(portfolio: pd.DataFrame) -> float:
    """Calculate total portfolio market value from quantity and price."""

    values = portfolio["quantity"].astype(float) * portfolio["price"].astype(float)
    return float(values.sum())


def asset_weights(portfolio: pd.DataFrame) -> pd.Series:
    """Calculate asset weights from portfolio market values."""

    values = portfolio.set_index("asset")["quantity"].astype(float) * portfolio.set_index("asset")[
        "price"
    ].astype(float)
    total = values.sum()
    if total <= 0:
        raise ValueError("Portfolio value must be positive.")
    return values / total


def asset_returns(prices: pd.DataFrame) -> pd.DataFrame:
    """Calculate simple daily asset returns from price history."""

    return prices.pct_change().dropna(how="all")


def portfolio_returns(prices: pd.DataFrame, weights: pd.Series) -> pd.Series:
    """Calculate daily portfolio returns from asset returns and weights."""

    returns = asset_returns(prices)
    aligned_weights = weights.reindex(returns.columns).fillna(0.0)
    return returns.mul(aligned_weights, axis=1).sum(axis=1)


def annualized_volatility(
    returns: pd.Series,
    periods_per_year: int = TRADING_DAYS_PER_YEAR,
) -> float:
    """Calculate annualized volatility from daily returns."""

    clean = returns.dropna()
    if clean.empty:
        return float("nan")
    return float(clean.std(ddof=1) * np.sqrt(periods_per_year))


def drawdown_series(returns: pd.Series) -> pd.Series:
    """Calculate drawdown series from returns."""

    clean = returns.fillna(0.0)
    equity = (1.0 + clean).cumprod()
    running_max = equity.cummax()
    return equity / running_max - 1.0


def max_drawdown(returns: pd.Series) -> float:
    """Calculate maximum drawdown from returns."""

    drawdowns = drawdown_series(returns)
    if drawdowns.empty:
        return float("nan")
    return float(drawdowns.min())


def historical_var(returns: pd.Series, level: float = 0.95) -> float:
    """Calculate historical Value at Risk as a positive loss number."""

    clean = returns.dropna()
    if clean.empty:
        return float("nan")
    quantile = np.quantile(clean, 1.0 - level)
    return float(max(0.0, -quantile))


def historical_cvar(returns: pd.Series, level: float = 0.95) -> float:
    """Calculate historical Conditional Value at Risk as a positive loss number."""

    clean = returns.dropna()
    if clean.empty:
        return float("nan")
    threshold = np.quantile(clean, 1.0 - level)
    tail = clean[clean <= threshold]
    if tail.empty:
        return float("nan")
    return float(max(0.0, -tail.mean()))


def correlation_matrix(prices: pd.DataFrame) -> pd.DataFrame:
    """Calculate asset return correlation matrix."""

    returns = asset_returns(prices)
    return returns.corr()


def simple_stress_tests(weights: pd.Series, portfolio_total: float) -> list[dict[str, float | str]]:
    """Run simple portfolio stress tests using uniform asset shocks."""

    scenarios = {
        "broad_market_minus_10pct": -0.10,
        "broad_market_minus_20pct": -0.20,
        "risk_assets_minus_30pct": -0.30,
    }
    gross_exposure = float(weights.abs().sum())
    results: list[dict[str, float | str]] = []
    for scenario, shock in scenarios.items():
        portfolio_pnl = portfolio_total * gross_exposure * shock
        results.append(
            {
                "scenario": scenario,
                "shock": shock,
                "portfolio_pnl": float(portfolio_pnl),
                "portfolio_pnl_pct": float(portfolio_pnl / portfolio_total),
            }
        )
    return results
