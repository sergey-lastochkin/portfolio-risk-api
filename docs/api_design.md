# API Design

Stage 1 exposes a small path-based CSV API.

## `GET /health`

Returns service status.

Example:

```json
{
  "status": "ok"
}
```

## `GET /metadata`

Returns project metadata, limitations, and implemented endpoints.

Example:

```bash
curl http://127.0.0.1:8000/metadata
```

## `POST /risk/summary`

Calculates a compact risk summary.

Request:

```json
{
  "portfolio_path": "data/sample_portfolio.csv",
  "prices_path": "data/sample_prices.csv",
  "var_level": 0.95
}
```

Response includes:

- portfolio value;
- weights;
- annualized volatility;
- max drawdown;
- VaR 95%;
- CVaR 95%;
- observations;
- stress tests;
- limitations.

Example:

```bash
curl -X POST http://127.0.0.1:8000/risk/summary \
  -H "Content-Type: application/json" \
  -d '{"portfolio_path":"data/sample_portfolio.csv","prices_path":"data/sample_prices.csv"}'
```

Compact response shape:

```json
{
  "portfolio_value": 27800.0,
  "weights": {
    "AAPL": 0.0683
  },
  "annualized_volatility": 0.067,
  "max_drawdown": -0.012,
  "var_95": 0.004,
  "cvar_95": 0.006,
  "observations": 29,
  "stress_tests": [],
  "limitations": []
}
```

VaR and CVaR are positive loss numbers.

## `POST /risk/report`

Returns the fuller report, including the correlation matrix, notes, and limitations.

Example:

```bash
curl -X POST http://127.0.0.1:8000/risk/report \
  -H "Content-Type: application/json" \
  -d '{"portfolio_path":"data/sample_portfolio.csv","prices_path":"data/sample_prices.csv"}'
```

## Error Behavior

The API returns HTTP 400 with a readable `detail` message for:

- missing files;
- invalid CSV schema;
- missing required columns;
- insufficient price history;
- non-numeric, missing, zero, or negative prices;
- portfolio assets missing from the price history.

## Future API Direction

Later stages can add file upload, stronger schemas, richer scenario inputs, and report export.
