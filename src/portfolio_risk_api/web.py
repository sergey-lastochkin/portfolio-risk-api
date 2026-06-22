"""Helpers for the lightweight public HTML demo."""

from pathlib import Path
from typing import Any

from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from jinja2 import pass_context

from portfolio_risk_api.localization import normalize_language, ui_text

PACKAGE_DIR = Path(__file__).resolve().parent
STATIC_DIR = PACKAGE_DIR / "static"
TEMPLATES_DIR = PACKAGE_DIR / "templates"
templates = Jinja2Templates(directory=TEMPLATES_DIR)


def sample_data_path(filename: str) -> Path:
    """Resolve a repository sample file in local and Docker environments."""

    candidates = [
        Path.cwd() / "data" / filename,
        PACKAGE_DIR.parents[1] / "data" / filename,
    ]
    return next((path for path in candidates if path.is_file()), candidates[0])


@pass_context
def _number(context: dict[str, Any], value: Any) -> str:
    if value is None:
        return "нет данных" if context.get("lang") == "ru" else "n/a"
    formatted = f"{float(value):,.2f}"
    return (
        formatted.replace(",", " ").replace(".", ",") if context.get("lang") == "ru" else formatted
    )


@pass_context
def _percent(context: dict[str, Any], value: Any) -> str:
    if value is None:
        return "нет данных" if context.get("lang") == "ru" else "n/a"
    formatted = f"{float(value) * 100:.2f}%"
    return formatted.replace(".", ",") if context.get("lang") == "ru" else formatted


RU_LABELS = {
    "all_assets_down_5pct": "Все активы -5%",
    "all_assets_down_10pct": "Все активы -10%",
    "equity_down_10pct": "Акции -10%",
    "crypto_down_20pct": "Криптоактивы -20%",
    "fx_move_2pct": "Валюты -2%",
    "equity": "Акции",
    "crypto": "Криптоактивы",
    "fx": "Валюты",
    "other": "Прочее",
}

EN_LABELS = {
    "all_assets_down_5pct": "All assets -5%",
    "all_assets_down_10pct": "All assets -10%",
    "equity_down_10pct": "Equities -10%",
    "crypto_down_20pct": "Crypto assets -20%",
    "fx_move_2pct": "FX -2%",
    "equity": "Equity",
    "crypto": "Crypto",
    "fx": "FX",
    "other": "Other",
}


@pass_context
def _display_label(context: dict[str, Any], value: Any) -> str:
    normalized = str(value).strip().lower()
    labels = RU_LABELS if context.get("lang") == "ru" else EN_LABELS
    return labels.get(normalized, str(value).replace("_", " ").strip().title())


@pass_context
def _display_date(context: dict[str, Any], value: Any) -> str:
    text = str(value)
    parts = text.split("-")
    if context.get("lang") == "ru" and len(parts) == 3:
        return ".".join(reversed(parts))
    return text


def _stress_width(value: Any) -> str:
    if value is None:
        return "0"
    return f"{min(abs(float(value)) * 500, 100):.2f}"


@pass_context
def _source_label(context: dict[str, Any], value: Any) -> str:
    text = str(value)
    if text.startswith("upload:"):
        prefix = "Загруженный файл" if context.get("lang") == "ru" else "Uploaded file"
        return f"{prefix} · {text.removeprefix('upload:')}"
    filename = Path(text).name
    labels = (
        {
            "sample_portfolio.csv": "Синтетический портфель · sample_portfolio.csv",
            "sample_prices.csv": "Синтетическая история · sample_prices.csv",
        }
        if context.get("lang") == "ru"
        else {
            "sample_portfolio.csv": "Synthetic portfolio · sample_portfolio.csv",
            "sample_prices.csv": "Synthetic history · sample_prices.csv",
        }
    )
    fallback = "нет данных" if context.get("lang") == "ru" else "n/a"
    return labels.get(filename, filename or fallback)


templates.env.filters["number"] = _number
templates.env.filters["percent"] = _percent
templates.env.filters["display_label"] = _display_label
templates.env.filters["display_date"] = _display_date
templates.env.filters["stress_width"] = _stress_width
templates.env.filters["source_label"] = _source_label


ERROR_TRANSLATIONS = {
    "Portfolio CSV is empty.": "CSV портфеля пуст.",
    "Prices CSV is empty.": "CSV с историей цен пуст.",
    "Portfolio CSV contains empty asset names.": "В портфеле есть пустые названия активов.",
    "Portfolio CSV contains non-numeric quantity or price values.": (
        "В портфеле есть нечисловые значения количества или цены."
    ),
    "Portfolio CSV contains negative quantities.": "В портфеле есть отрицательное количество.",
    "Portfolio CSV contains non-positive prices.": (
        "В портфеле есть нулевые или отрицательные цены."
    ),
    "Prices CSV contains invalid dates.": "В истории цен есть некорректные даты.",
    "Prices CSV contains duplicate dates.": "В истории цен повторяются даты.",
    "Prices CSV contains non-numeric or missing prices.": (
        "В истории есть пропущенные или нечисловые цены."
    ),
    "Prices CSV contains non-positive prices.": "В истории есть нулевые или отрицательные цены.",
}


def localize_validation_error(message: str, language: str) -> str:
    """Translate common upload validation errors for the Russian public UI."""

    if normalize_language(language) != "ru":
        return message

    if message in ERROR_TRANSLATIONS:
        return ERROR_TRANSLATIONS[message]
    replacements = {
        "Portfolio CSV missing columns:": "В CSV портфеля отсутствуют колонки:",
        "Prices CSV missing columns:": "В CSV с историей цен отсутствуют колонки:",
        "Portfolio CSV contains duplicated assets:": "В портфеле повторяются активы:",
        "Prices CSV missing portfolio assets:": "В истории цен нет активов из портфеля:",
        "Uploaded file is empty:": "Загруженный файл пуст:",
        "Uploaded file must be a CSV:": "Нужен файл в формате CSV:",
        "Invalid CSV upload:": "Не удалось прочитать CSV:",
        "Prices CSV contains insufficient price history:": "Недостаточно истории цен:",
    }
    localized = message
    for source, target in replacements.items():
        localized = localized.replace(source, target)
    return localized


def render_template(
    request: Request,
    name: str,
    context: dict[str, Any] | None = None,
    status_code: int = 200,
) -> HTMLResponse:
    """Render a project template with shared context."""

    language = normalize_language(request.query_params.get("lang"))
    return templates.TemplateResponse(
        request=request,
        name=name,
        context={
            "github_url": "https://github.com/sergey-lastochkin/portfolio-risk-api",
            "lang": language,
            "ui": ui_text(language),
            **(context or {}),
        },
        status_code=status_code,
    )
