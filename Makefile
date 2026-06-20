.PHONY: install test lint format api check

PYTHON ?= .venv/bin/python
RUFF ?= .venv/bin/ruff
BLACK ?= .venv/bin/black
UVICORN ?= .venv/bin/uvicorn

install:
	python -m venv .venv
	$(PYTHON) -m pip install -e ".[dev]"

test:
	$(PYTHON) -m pytest -q

lint:
	$(RUFF) check .
	$(BLACK) --check .

format:
	$(BLACK) .
	$(RUFF) check . --fix

api:
	$(UVICORN) portfolio_risk_api.app:app --reload

check:
	$(PYTHON) -m compileall src tests
	$(PYTHON) -m pytest -q
	$(RUFF) check .
	$(BLACK) --check .
