"""FastAPI application for Portfolio Risk API."""

from typing import Annotated

from fastapi import FastAPI, File, HTTPException, Query, Request, UploadFile
from fastapi.exception_handlers import request_validation_exception_handler
from fastapi.exceptions import RequestValidationError
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles

from portfolio_risk_api import __version__
from portfolio_risk_api.config import path_endpoints_enabled
from portfolio_risk_api.data_loader import (
    DataValidationError,
    load_portfolio_upload,
    load_prices_upload,
)
from portfolio_risk_api.localization import normalize_language, ui_text
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
from portfolio_risk_api.web import (
    STATIC_DIR,
    localize_validation_error,
    render_template,
    sample_data_path,
)

app = FastAPI(
    title="Portfolio Risk API",
    description="Reusable backend for portfolio risk calculations from CSV data.",
    version=__version__,
)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

CsvUpload = Annotated[UploadFile, File(...)]


def _request_language(request: Request) -> str:
    return normalize_language(request.query_params.get("lang"))


@app.exception_handler(RequestValidationError)
async def validation_error_handler(request: Request, exc: RequestValidationError):
    """Use a friendly HTML validation error for the public upload form."""

    if request.url.path == "/demo/report":
        language = _request_language(request)
        return render_template(
            request,
            "error.html",
            {"message": ui_text(language)["error"]["missing_files"]},
            status_code=422,
        )
    return await request_validation_exception_handler(request, exc)


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def root(request: Request) -> HTMLResponse:
    """Render the synthetic sample report as the public demo."""

    portfolio_path = sample_data_path("sample_portfolio.csv")
    prices_path = sample_data_path("sample_prices.csv")
    try:
        report = build_risk_report(str(portfolio_path), str(prices_path))
    except DataValidationError as exc:
        return render_template(
            request,
            "error.html",
            {"message": localize_validation_error(str(exc), _request_language(request))},
            status_code=500,
        )
    return render_template(
        request,
        "report.html",
        {"report": report, "is_sample": True},
    )


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


@app.get("/demo", response_class=HTMLResponse, include_in_schema=False)
def demo(request: Request) -> HTMLResponse:
    """Render the CSV upload demo page."""

    return render_template(request, "demo.html")


def _sample_file_response(request: Request, filename: str) -> FileResponse | HTMLResponse:
    path = sample_data_path(filename)
    if not path.is_file():
        return render_template(
            request,
            "error.html",
            {
                "message": (
                    f"{ui_text(_request_language(request))['error']['sample_unavailable']}: "
                    f"{filename}"
                )
            },
            status_code=404,
        )
    return FileResponse(path, media_type="text/csv", filename=filename)


@app.get("/samples/portfolio.csv", response_model=None, include_in_schema=False)
def sample_portfolio(request: Request) -> FileResponse | HTMLResponse:
    """Download the synthetic sample portfolio CSV."""

    return _sample_file_response(request, "sample_portfolio.csv")


@app.get("/samples/prices.csv", response_model=None, include_in_schema=False)
def sample_prices(request: Request) -> FileResponse | HTMLResponse:
    """Download the synthetic sample price history CSV."""

    return _sample_file_response(request, "sample_prices.csv")


@app.get("/demo/sample-report", response_class=HTMLResponse, include_in_schema=False)
def demo_sample_report(request: Request) -> HTMLResponse:
    """Render a report using the repository's synthetic sample data."""

    portfolio_path = sample_data_path("sample_portfolio.csv")
    prices_path = sample_data_path("sample_prices.csv")
    try:
        report = build_risk_report(str(portfolio_path), str(prices_path))
    except DataValidationError as exc:
        return render_template(
            request,
            "error.html",
            {"message": localize_validation_error(str(exc), _request_language(request))},
            status_code=500,
        )
    return render_template(
        request,
        "report.html",
        {"report": report, "is_sample": True},
    )


@app.post("/demo/report", response_class=HTMLResponse, include_in_schema=False)
async def demo_uploaded_report(
    request: Request,
    portfolio_file: CsvUpload,
    prices_file: CsvUpload,
) -> HTMLResponse:
    """Render a report from uploaded CSV files without storing them."""

    try:
        report = await _uploaded_report(portfolio_file, prices_file, 0.95)
    except HTTPException as exc:
        return render_template(
            request,
            "error.html",
            {
                "message": localize_validation_error(
                    str(exc.detail),
                    _request_language(request),
                )
            },
            status_code=exc.status_code,
        )
    return render_template(
        request,
        "report.html",
        {"report": report, "is_sample": False},
    )
