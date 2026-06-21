# API Design

Stage 2 exposes a small CSV API with both path-based inputs and multipart file uploads.

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

Returns the fuller report, including correlation, concentration, top positions, stress scenarios, provenance, notes, and limitations.

Example:

```bash
curl -X POST http://127.0.0.1:8000/risk/report \
  -H "Content-Type: application/json" \
  -d '{"portfolio_path":"data/sample_portfolio.csv","prices_path":"data/sample_prices.csv"}'
```

Report response includes:

- `portfolio_value`
- `weights`
- `annualized_volatility`
- `max_drawdown`
- `var_95`
- `cvar_95`
- `correlation_matrix`
- `stress_tests`
- `concentration`
- `top_positions`
- `largest_notional_contributors`
- `coverage`
- `provenance`
- `notes`
- `limitations`

## `POST /risk/summary/upload`

Calculates the same compact summary from uploaded CSV files.

Example:

```bash
curl -X POST http://127.0.0.1:8000/risk/summary/upload \
  -F "portfolio_file=@data/sample_portfolio.csv" \
  -F "prices_file=@data/sample_prices.csv"
```

## `POST /risk/report/upload`

Calculates the fuller report from uploaded CSV files.

Example:

```bash
curl -X POST http://127.0.0.1:8000/risk/report/upload \
  -F "portfolio_file=@data/sample_portfolio.csv" \
  -F "prices_file=@data/sample_prices.csv"
```

## Portfolio CSV Schema

Required columns:

- `asset`
- `quantity`
- `price`

Optional column:

- `asset_class`

If `asset_class` is missing, the API infers a coarse class from the asset name. For example, BTC is treated as crypto, EURUSD as FX, and AAPL as equity.

## Error Behavior

The API returns HTTP 400 with a readable `detail` message for:

- missing files;
- empty uploads;
- wrong uploaded file type;
- invalid CSV schema;
- missing required columns;
- insufficient price history;
- non-numeric, missing, zero, or negative prices;
- duplicated portfolio assets;
- portfolio assets missing from the price history.

## Future API Direction

Later stages can add user-defined scenario inputs, richer error response objects, market data adapters, and report export.
