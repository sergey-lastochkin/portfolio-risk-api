# Portfolio Risk API

Portfolio Risk API is a reusable backend for portfolio risk calculations across markets. It is designed to work with simple portfolio and price datasets, starting from CSV inputs and a small FastAPI service.

This is the second public project line after Russian Markets Lab.

- Russian Markets Lab: market data, MOEX, research dashboard.
- Portfolio Risk API: reusable risk backend across markets.

The project accepts a portfolio and historical price data, calculates first-pass risk metrics, and returns compact JSON reports that can later be used by dashboards, notebooks, internal tools, or scheduled reports.

## What It Does

- Loads portfolio CSV files.
- Loads historical price CSV files.
- Calculates portfolio weights.
- Builds portfolio returns.
- Calculates volatility, drawdown, VaR, CVaR, correlation, and simple stress scenarios.
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

## API Endpoints

Implemented in Stage 1:

- `GET /health`
- `GET /metadata`
- `POST /risk/summary`
- `POST /risk/report`

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
  "annualized_volatility": 0.067,
  "max_drawdown": -0.012,
  "var_95": 0.004,
  "cvar_95": 0.006,
  "observations": 29
}
```

`var_95` and `cvar_95` are reported as positive loss numbers, not as return quantiles.

## Portfolio Strategy Context

Portfolio Risk API is part of a broader line of market research tools:

- market data infrastructure;
- risk analytics;
- derivatives research;
- execution cost analysis;
- reusable APIs and reports.

MOEX was the first public case through Russian Markets Lab. This project moves the portfolio toward a market-agnostic risk backend while staying honest about the current Stage 1 scope.

## Limitations

- The included data is sample/synthetic.
- Historical risk metrics are backward-looking.
- VaR and CVaR do not predict future losses.
- Stress tests are simplified uniform shocks.
- No full margin, liquidity, tax, funding, or liquidation model is included.
- No broker connection or order execution is included.
- The API is not an investment advice or trading system.

## Status

Stage 1: CSV risk API MVP.

## Stage 2 Roadmap

Next work should focus on:

- richer report structure;
- stronger input validation;
- user-defined scenario definitions;
- optional file upload;
- cleaner adapters for different market data sources.
