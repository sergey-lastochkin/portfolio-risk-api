# Project Status

## Current Stage

Stage 1 MVP.

Portfolio Risk API is a small FastAPI backend for calculating portfolio risk metrics from CSV inputs.

## Implemented Endpoints

- `GET /health`
- `GET /metadata`
- `POST /risk/summary`
- `POST /risk/report`

## Implemented Metrics

- Portfolio value
- Asset weights
- Daily asset returns
- Daily portfolio returns
- Annualized volatility
- Maximum drawdown
- Historical VaR as a positive loss number
- Historical CVaR as a positive loss number
- Correlation matrix
- Simple stress tests

## Validation and Error Handling

The API and loaders handle:

- missing files;
- missing required portfolio columns;
- missing required price columns;
- invalid dates;
- duplicate dates;
- non-numeric prices;
- missing prices;
- zero or negative prices;
- insufficient price history;
- portfolio assets missing from the price history.

Validation errors are returned by the API as HTTP 400 responses with readable `detail` messages.

## Test Coverage Summary

The test suite covers:

- sample CSV loading;
- schema validation failures;
- NaN, zero, and negative price rejection;
- insufficient history rejection;
- unknown asset handling;
- asset weights;
- constant price behavior;
- drawdown behavior;
- VaR/CVaR sign convention;
- stress test output shape;
- health, metadata, summary, and report endpoints.

## Known Warning

The test suite currently shows a dependency-level FastAPI/Starlette warning:

```text
StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
```

The warning does not affect Stage 1 behavior. It should be revisited when the FastAPI/Starlette test client ecosystem settles or when moving to a pinned production dependency set.

## Limitations

- Included data is sample/synthetic.
- Historical metrics are backward-looking.
- VaR and CVaR do not predict future losses.
- Stress tests are simplified uniform shocks.
- No full broker margin model is included.
- No liquidity liquidation model is included.
- No broker connection or order execution is included.
- The API does not provide investment advice.

## Next Stage

Stage 2 should focus on richer reports, stronger schema validation, user-defined scenario inputs, optional file upload, and cleaner adapters for different market data sources.
