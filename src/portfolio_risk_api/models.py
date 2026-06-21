"""Pydantic models for the API."""

from pydantic import BaseModel, Field


class RiskRequest(BaseModel):
    """Request body for path-based CSV risk calculation."""

    portfolio_path: str = Field(
        default="data/sample_portfolio.csv",
        description=(
            "Path to a portfolio CSV file with asset, quantity, price, "
            "and optional asset_class columns."
        ),
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

    scenario_name: str
    portfolio_pnl: float
    portfolio_pnl_pct: float | None
    per_asset_impact: dict[str, float]


class PositionItem(BaseModel):
    """Position ranking item."""

    asset: str
    asset_class: str | None = None
    weight: float | None
    notional_value: float | None = None


class NotionalContributor(BaseModel):
    """Notional value contributor item."""

    asset: str
    notional_value: float | None
    weight: float | None


class ConcentrationMetrics(BaseModel):
    """Portfolio concentration metrics."""

    top_1_weight: float | None
    top_3_weight: float | None
    effective_number_of_positions: float | None


class CoverageMetadata(BaseModel):
    """Asset coverage metadata."""

    assets_in_portfolio: int
    assets_with_price_history: int
    missing_assets: list[str]


class DataWindow(BaseModel):
    """Price data window metadata."""

    start_date: str
    end_date: str
    observations: int


class ProvenanceMetadata(BaseModel):
    """Input provenance metadata."""

    portfolio_source: str
    prices_source: str
    data_window: DataWindow
    portfolio_columns: list[str]
    price_assets: list[str]


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
    concentration: ConcentrationMetrics
    top_positions: list[PositionItem]
    largest_notional_contributors: list[NotionalContributor]
    coverage: CoverageMetadata
    provenance: ProvenanceMetadata
    notes: list[str]
