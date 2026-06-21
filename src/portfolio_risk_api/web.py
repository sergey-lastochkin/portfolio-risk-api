"""Helpers for the lightweight public HTML demo."""

from pathlib import Path
from typing import Any

from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

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


def _number(value: Any) -> str:
    if value is None:
        return "n/a"
    return f"{float(value):,.2f}"


def _percent(value: Any) -> str:
    if value is None:
        return "n/a"
    return f"{float(value) * 100:.2f}%"


def _label(value: Any) -> str:
    return str(value).replace("_", " ").strip().title()


templates.env.filters["number"] = _number
templates.env.filters["percent"] = _percent
templates.env.filters["label"] = _label


def render_template(
    request: Request,
    name: str,
    context: dict[str, Any] | None = None,
    status_code: int = 200,
) -> HTMLResponse:
    """Render a project template with shared context."""

    return templates.TemplateResponse(
        request=request,
        name=name,
        context={
            "github_url": "https://github.com/sergey-lastochkin/portfolio-risk-api",
            **(context or {}),
        },
        status_code=status_code,
    )
