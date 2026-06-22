# Portfolio Risk API

Portfolio Risk API is a reusable backend for portfolio risk calculations across markets. It is designed to work with simple portfolio and price datasets, starting from CSV inputs and a small FastAPI service.

This is the second project in the portfolio after Russian Markets Lab.

- Russian Markets Lab: market data, MOEX, research dashboard.
- Portfolio Risk API: reusable risk backend across markets.

The project accepts a portfolio and historical price data, calculates first-pass risk metrics, and returns compact JSON reports that can later be used by dashboards, notebooks, internal tools, or scheduled reports.

## What It Does

- Loads portfolio CSV files.
- Loads historical price CSV files.
- Accepts path-based CSV inputs or multipart CSV uploads.
- Calculates portfolio weights.
- Builds portfolio returns.
- Calculates volatility, drawdown, VaR, CVaR, correlation, concentration, and stress scenarios.
- Exposes a small FastAPI service for risk summaries and reports.

## What It Does Not Do

- It does not provide investment advice.
- It does not send orders.
- It does not connect to brokers.
- It does not use private API keys.
- It does not promise alpha, trading signals, arbitrage, profit, or risk reduction.
- It does not predict future losses. Historical risk metrics are backward-looking.

## Data

The included files in `data/` are sample/synthetic examples. They are used to test the API shape and methodology. They should not be presented as real market research output.

## Quickstart

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
uvicorn portfolio_risk_api.app:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

## Run Tests

```bash
pytest -q
```

Full local checks:

```bash
make test
make lint
```

## Docker

```bash
docker build -t portfolio-risk-api .
docker run --rm -p 8000:8000 portfolio-risk-api
```

## Deployment

Local Docker remains supported and defaults to port `8000`. The container also reads Render's `PORT` environment variable and binds Uvicorn to `0.0.0.0`.

Render deployment instructions and smoke checks are documented in [`docs/deployment_render.md`](docs/deployment_render.md).

On Render, server-side path endpoints are disabled. Use the multipart upload endpoints from `/docs`. The hosted API is a demonstration and research tool. It does not provide investment advice and is not a trading system.

Live API:

- Public demo: https://portfolio-risk-api-eb40.onrender.com
- Russian demo: https://portfolio-risk-api-eb40.onrender.com/?lang=ru
- CSV upload page: https://portfolio-risk-api-eb40.onrender.com/demo
- Sample report: https://portfolio-risk-api-eb40.onrender.com/demo/sample-report
- Swagger UI: https://portfolio-risk-api-eb40.onrender.com/docs
- Health: https://portfolio-risk-api-eb40.onrender.com/health

The free Render instance can take up to about 50 seconds to wake after inactivity.

The web pages are a lightweight public demo over the same report functions used by the API. English is the default interface language, with Russian available through the EN/RU switch or `?lang=ru`. Visitors can inspect a synthetic sample report, download sample CSV files, or upload their own files without adding accounts, storage, or a trading workflow. The demo does not provide investment advice, a trading system, or trading signals.

## API Endpoints

Implemented:

- `GET /`
- `GET /demo`
- `GET /demo/sample-report`
- `POST /demo/report`
- `GET /samples/portfolio.csv`
- `GET /samples/prices.csv`
- `GET /health`
- `GET /metadata`
- `POST /risk/summary`
- `POST /risk/report`
- `POST /risk/summary/upload`
- `POST /risk/report/upload`

The risk endpoints accept JSON paths to CSV files:

```json
{
  "portfolio_path": "data/sample_portfolio.csv",
  "prices_path": "data/sample_prices.csv"
}
```

## Example API Calls

Health:

```bash
curl http://127.0.0.1:8000/health
```

Metadata:

```bash
curl http://127.0.0.1:8000/metadata
```

Risk summary:

```bash
curl -X POST http://127.0.0.1:8000/risk/summary \
  -H "Content-Type: application/json" \
  -d '{"portfolio_path":"data/sample_portfolio.csv","prices_path":"data/sample_prices.csv"}'
```

Risk report:

```bash
curl -X POST http://127.0.0.1:8000/risk/report \
  -H "Content-Type: application/json" \
  -d '{"portfolio_path":"data/sample_portfolio.csv","prices_path":"data/sample_prices.csv"}'
```

Risk summary from uploaded CSV files:

```bash
curl -X POST http://127.0.0.1:8000/risk/summary/upload \
  -F "portfolio_file=@data/sample_portfolio.csv" \
  -F "prices_file=@data/sample_prices.csv"
```

Risk report from uploaded CSV files:

```bash
curl -X POST http://127.0.0.1:8000/risk/report/upload \
  -F "portfolio_file=@data/sample_portfolio.csv" \
  -F "prices_file=@data/sample_prices.csv"
```

Compact example response:

```json
{
  "portfolio_value": 27800.0,
  "weights": {
    "AAPL": 0.0683,
    "MSFT": 0.0755,
    "BTC": 0.4676,
    "EURUSD": 0.3885
  },
  "annualized_volatility": 0.0987,
  "max_drawdown": -0.006,
  "var_95": 0.0052,
  "cvar_95": 0.0057,
  "observations": 29
}
```

`var_95` and `cvar_95` are reported as positive loss numbers, not as return quantiles.
The Stage 2 API fixes the confidence level at 95% so the calculation matches these response field names.

The full report also includes:

- correlation matrix;
- deterministic stress scenarios;
- concentration metrics;
- top positions by weight;
- largest notional contributors;
- asset coverage;
- input provenance and data window metadata.

`asset_class` is optional in the portfolio CSV. If it is missing, the loader infers a coarse class from the asset name, for example BTC as crypto, EURUSD as FX, and AAPL as equity.

## Portfolio Strategy Context

Portfolio Risk API is part of a broader line of market research tools:

- market data infrastructure;
- risk analytics;
- derivatives research;
- execution cost analysis;
- reusable APIs and reports.

MOEX was the first public case through Russian Markets Lab. The input schema here is not tied to one exchange. The current implementation remains a Stage 2 local MVP built around CSV inputs and simplified historical risk methods.

## Limitations

- The included data is sample/synthetic.
- Historical risk metrics are backward-looking.
- VaR and CVaR do not predict future losses.
- Stress tests are simplified deterministic shocks.
- No full margin, liquidity, tax, funding, or liquidation model is included.
- No broker connection or order execution is included.
- The API is not an investment advice or trading system.
- Path-based endpoints are intended for local or trusted environments. External clients should use upload endpoints rather than arbitrary server file paths.
- Position values are assumed to share one portfolio valuation currency. Currency conversion is not modeled.

## Status

Stage 2 local: CSV risk API with upload support, richer report structure, and deterministic scenario diagnostics.

## Stage 3 Roadmap

Next work should focus on:

- user-defined scenario definitions;
- richer error response objects;
- cleaner adapters for different market data sources;
- optional dashboard or hosted API demo later.
