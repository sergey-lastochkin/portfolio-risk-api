"""FastAPI application for Portfolio Risk API."""

from fastapi import FastAPI, HTTPException

from portfolio_risk_api import __version__
from portfolio_risk_api.data_loader import DataValidationError
from portfolio_risk_api.models import (
    HealthResponse,
    MetadataResponse,
    RiskReportResponse,
    RiskRequest,
    RiskSummaryResponse,
)
from portfolio_risk_api.report import build_risk_report, build_risk_summary

app = FastAPI(
    title="Portfolio Risk API",
    description="Reusable backend for portfolio risk calculations from CSV data.",
    version=__version__,
)


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    """Return API health status."""

    return HealthResponse(status="ok")


@app.get("/metadata", response_model=MetadataResponse)
def metadata() -> MetadataResponse:
    """Return project metadata and limitations."""

    return MetadataResponse(
        name="Portfolio Risk API",
        version=__version__,
        positioning="Reusable backend for portfolio risk calculations across markets.",
        limitations=[
            "No investment advice.",
            "No broker connection.",
            "No live trading.",
            "Sample data is synthetic.",
        ],
        implemented_endpoints=[
            "GET /health",
            "GET /metadata",
            "POST /risk/summary",
            "POST /risk/report",
        ],
    )


@app.post("/risk/summary", response_model=RiskSummaryResponse)
def risk_summary(request: RiskRequest) -> RiskSummaryResponse:
    """Return a compact risk summary."""

    try:
        return RiskSummaryResponse(
            **build_risk_summary(
                request.portfolio_path,
                request.prices_path,
                request.var_level,
            )
        )
    except DataValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/risk/report", response_model=RiskReportResponse)
def risk_report(request: RiskRequest) -> RiskReportResponse:
    """Return a full risk report."""

    try:
        return RiskReportResponse(
            **build_risk_report(
                request.portfolio_path,
                request.prices_path,
                request.var_level,
            )
        )
    except DataValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
