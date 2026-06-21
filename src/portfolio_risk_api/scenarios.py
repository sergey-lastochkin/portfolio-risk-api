"""Simple deterministic portfolio stress scenarios."""

from typing import Any

import pandas as pd

from portfolio_risk_api.data_loader import infer_asset_class
from portfolio_risk_api.risk_metrics import portfolio_value

SCENARIO_SHOCKS: dict[str, dict[str, float]] = {
    "all_assets_down_5pct": {"all": -0.05},
    "all_assets_down_10pct": {"all": -0.10},
    "equity_down_10pct": {"equity": -0.10},
    "crypto_down_20pct": {"crypto": -0.20},
    "fx_move_2pct": {"fx": -0.02},
}


def asset_class_map(portfolio: pd.DataFrame) -> dict[str, str]:
    """Return a coarse asset class map for portfolio assets."""

    if "asset_class" in portfolio.columns:
        return {
            str(row["asset"]): str(row["asset_class"] or infer_asset_class(row["asset"])).lower()
            for _, row in portfolio.iterrows()
        }
    return {str(asset): infer_asset_class(str(asset)) for asset in portfolio["asset"]}


def run_stress_scenarios(portfolio: pd.DataFrame) -> list[dict[str, Any]]:
    """Run deterministic shocks and return portfolio and per-asset impact."""

    total_value = portfolio_value(portfolio)
    classes = asset_class_map(portfolio)
    notionals = portfolio["quantity"].astype(float) * portfolio["price"].astype(float)
    values = portfolio.assign(notional=notionals).set_index("asset")["notional"].astype(float)

    results: list[dict[str, Any]] = []
    for scenario_name, shocks in SCENARIO_SHOCKS.items():
        per_asset_impact: dict[str, float] = {}
        for asset, notional in values.items():
            asset_class = classes.get(str(asset), infer_asset_class(str(asset)))
            shock = shocks.get("all", shocks.get(asset_class, 0.0))
            per_asset_impact[str(asset)] = float(notional * shock)
        portfolio_pnl = float(sum(per_asset_impact.values()))
        results.append(
            {
                "scenario_name": scenario_name,
                "portfolio_pnl": portfolio_pnl,
                "portfolio_pnl_pct": float(portfolio_pnl / total_value) if total_value else None,
                "per_asset_impact": per_asset_impact,
            }
        )
    return results
