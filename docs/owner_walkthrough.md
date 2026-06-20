# Owner Walkthrough

This document explains how Portfolio Risk API is wired internally.

## Project Shape

The project is a small FastAPI backend.

Main folders:

- `src/portfolio_risk_api/` contains the application code.
- `data/` contains sample CSV inputs.
- `tests/` contains unit and API tests.
- `docs/` contains methodology, status, and owner notes.

The project does not call brokers, does not use market data APIs, and does not send orders. Stage 1 works from local CSV files.

## Data Path

The normal path is:

```text
portfolio CSV + prices CSV
-> data_loader.py
-> risk_metrics.py
-> report.py
-> app.py
-> JSON API response
```

The API receives paths to two CSV files:

- portfolio file with `asset`, `quantity`, `price`;
- prices file with `date` and one column per asset.

The loader validates the files, the metrics module calculates risk numbers, the report module assembles a response, and the FastAPI app returns JSON.

## `data_loader.py`

This file is responsible for reading and validating CSV inputs.

It checks:

- portfolio file exists;
- prices file exists;
- required columns are present;
- dates are valid;
- dates are not duplicated;
- numeric fields can be parsed;
- prices are not missing;
- prices are positive;
- there is enough price history;
- every portfolio asset exists in the price file.

If something is wrong, it raises `DataValidationError` with a readable message.

## `risk_metrics.py`

This file contains the core math.

It calculates:

- portfolio value;
- asset weights;
- asset returns;
- portfolio returns;
- annualized volatility;
- drawdown series;
- max drawdown;
- historical VaR;
- historical CVaR;
- correlation matrix;
- simple stress tests.

The important convention is:

```text
VaR and CVaR are returned as positive loss numbers.
```

If the return quantile is `-0.02`, the API reports `0.02`.

## `report.py`

This file connects loaders and metrics.

It:

1. loads portfolio CSV;
2. loads price CSV;
3. checks that prices cover all portfolio assets;
4. calculates weights and portfolio returns;
5. calculates risk metrics;
6. assembles a compact Python dictionary.

There are two report functions:

- `build_risk_summary(...)` for a smaller API response;
- `build_risk_report(...)` for a fuller response with correlation, notes, and limitations.

## `app.py`

This file exposes the FastAPI app.

Endpoints:

- `GET /health`
- `GET /metadata`
- `POST /risk/summary`
- `POST /risk/report`

If validation fails, `app.py` converts `DataValidationError` into HTTP 400 with a readable `detail` field.

## Pydantic Models

Pydantic models live in `models.py`.

They define:

- request body for risk endpoints;
- health response;
- metadata response;
- stress test response item;
- summary response;
- full report response.

The models make the API contract more explicit and make FastAPI docs cleaner.

## Important Tests

The tests protect the parts most likely to break silently.

`test_data_loader.py` checks:

- sample files load;
- missing columns fail;
- missing prices fail;
- zero or negative prices fail;
- short price history fails;
- unknown assets fail.

`test_risk_metrics.py` checks:

- weights sum to 1;
- constant prices produce zero returns and near-zero volatility;
- falling prices produce negative drawdown;
- VaR/CVaR are positive loss numbers;
- stress test output keys stay stable.

`test_api.py` checks:

- `/health`;
- `/metadata`;
- `/risk/summary`;
- `/risk/report`;
- validation errors through the API.

## How To Explain It Simply

This is a backend that takes portfolio and price tables, checks that they are usable, calculates basic historical risk metrics, and returns a JSON risk report.

It is not a trading system. It is not a prediction model. It is a clean risk calculation layer that can later sit behind dashboards, reports, or internal tools.
