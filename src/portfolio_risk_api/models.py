"""Pydantic models for the API."""

from pydantic import BaseModel, Field


class RiskRequest(BaseModel):
    """Request body for path-based CSV risk calculation."""

    portfolio_path: str = Field(
        default="data/sample_portfolio.csv",
        description="Path to a portfolio CSV file with asset, quantity, and price columns.",
    )
    prices_path: str = Field(
        default="data/sample_prices.csv",
        description="Path to a price CSV file with date and one column per asset.",
    )
    var_level: float = Field(default=0.95, ge=0.5, lt=1.0)


class HealthResponse(BaseModel):
    """Health check response."""

    status: str


class MetadataResponse(BaseModel):
    """Project metadata response."""

    name: str
    version: str
    positioning: str
    limitations: list[str]
    implemented_endpoints: list[str]


class StressTestResult(BaseModel):
    """Stress test result item."""

    scenario: str
    shock: float
    portfolio_pnl: float
    portfolio_pnl_pct: float


class RiskSummaryResponse(BaseModel):
    """Compact risk summary response."""

    portfolio_value: float
    weights: dict[str, float | None]
    annualized_volatility: float | None
    max_drawdown: float | None
    var_95: float | None
    cvar_95: float | None
    observations: int
    stress_tests: list[StressTestResult]
    limitations: list[str]


class RiskReportResponse(RiskSummaryResponse):
    """Full risk report response."""

    correlation_matrix: dict[str, dict[str, float | None]]
    notes: list[str]
