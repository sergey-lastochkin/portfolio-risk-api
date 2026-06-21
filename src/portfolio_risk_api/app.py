"""FastAPI application for Portfolio Risk API."""

from typing import Annotated

from fastapi import FastAPI, File, HTTPException, Query, UploadFile
from fastapi.responses import RedirectResponse

from portfolio_risk_api import __version__
from portfolio_risk_api.config import path_endpoints_enabled
from portfolio_risk_api.data_loader import (
    DataValidationError,
    load_portfolio_upload,
    load_prices_upload,
)
from portfolio_risk_api.models import (
    HealthResponse,
    MetadataResponse,
    RiskReportResponse,
    RiskRequest,
    RiskSummaryResponse,
)
from portfolio_risk_api.report import (
    build_risk_report,
    build_risk_report_from_frames,
    build_risk_summary,
    build_risk_summary_from_report,
)

app = FastAPI(
    title="Portfolio Risk API",
    description="Reusable backend for portfolio risk calculations from CSV data.",
    version=__version__,
)

CsvUpload = Annotated[UploadFile, File(...)]


@app.get("/", include_in_schema=False)
def root() -> RedirectResponse:
    """Open the interactive API documentation from the service root."""

    return RedirectResponse(url="/docs")


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    """Return API health status."""

    return HealthResponse(status="ok")


@app.get("/metadata", response_model=MetadataResponse)
def metadata() -> MetadataResponse:
    """Return project metadata and limitations."""

    endpoints = [
        "GET /health",
        "GET /metadata",
        "POST /risk/summary/upload",
        "POST /risk/report/upload",
    ]
    limitations = [
        "No investment advice.",
        "No broker connection.",
        "No live trading.",
        "Sample data is synthetic.",
    ]
    if path_endpoints_enabled():
        endpoints[2:2] = ["POST /risk/summary", "POST /risk/report"]
    else:
        limitations.append(
            "Path-based endpoints are disabled on Render; use multipart upload endpoints."
        )
    return MetadataResponse(
        name="Portfolio Risk API",
        version=__version__,
        positioning="Reusable backend for portfolio risk calculations across markets.",
        limitations=limitations,
        implemented_endpoints=endpoints,
    )


def _require_path_endpoints() -> None:
    if not path_endpoints_enabled():
        raise HTTPException(
            status_code=403,
            detail=(
                "Path-based endpoints are disabled in this hosted deployment. "
                "Use /risk/summary/upload or /risk/report/upload."
            ),
        )


@app.post("/risk/summary", response_model=RiskSummaryResponse)
def risk_summary(request: RiskRequest) -> RiskSummaryResponse:
    """Return a compact risk summary."""

    _require_path_endpoints()
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


async def _uploaded_report(
    portfolio_file: UploadFile,
    prices_file: UploadFile,
    var_level: float,
) -> dict:
    try:
        portfolio_content = await portfolio_file.read()
        prices_content = await prices_file.read()
        portfolio = load_portfolio_upload(portfolio_content, portfolio_file.filename)
        prices = load_prices_upload(prices_content, prices_file.filename)
        return build_risk_report_from_frames(
            portfolio,
            prices,
            var_level,
            portfolio_source=f"upload:{portfolio_file.filename or 'portfolio_file'}",
            prices_source=f"upload:{prices_file.filename or 'prices_file'}",
        )
    except DataValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/risk/summary/upload", response_model=RiskSummaryResponse)
async def risk_summary_upload(
    portfolio_file: CsvUpload,
    prices_file: CsvUpload,
    var_level: Annotated[float, Query(ge=0.95, le=0.95)] = 0.95,
) -> RiskSummaryResponse:
    """Return a compact risk summary from uploaded CSV files."""

    report = await _uploaded_report(portfolio_file, prices_file, var_level)
    return RiskSummaryResponse(**build_risk_summary_from_report(report))


@app.post("/risk/report/upload", response_model=RiskReportResponse)
async def risk_report_upload(
    portfolio_file: CsvUpload,
    prices_file: CsvUpload,
    var_level: Annotated[float, Query(ge=0.95, le=0.95)] = 0.95,
) -> RiskReportResponse:
    """Return a full risk report from uploaded CSV files."""

    report = await _uploaded_report(portfolio_file, prices_file, var_level)
    return RiskReportResponse(**report)


@app.post("/risk/report", response_model=RiskReportResponse)
def risk_report(request: RiskRequest) -> RiskReportResponse:
    """Return a full risk report."""

    _require_path_endpoints()
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
