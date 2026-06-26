# Project Status

## Current Stage

Stage 2 local MVP.

Portfolio Risk API is a small FastAPI backend for calculating portfolio risk metrics from CSV inputs. It supports path-based sample inputs and multipart CSV uploads.

## Implemented Endpoints

- `GET /health`
- `GET /metadata`
- `POST /risk/summary`
- `POST /risk/report`
- `POST /risk/summary/upload`
- `POST /risk/report/upload`

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
- Deterministic stress scenarios
- Concentration metrics
- Top positions by weight
- Largest notional contributors
- Asset coverage metadata
- Input provenance and data window metadata

## Validation and Error Handling

The API and loaders handle:

- missing files;
- uploads larger than the 5 MB per-file limit;
- missing required portfolio columns;
- missing required price columns;
- invalid dates;
- duplicate dates;
- non-numeric prices;
- missing prices;
- zero or negative prices;
- insufficient price history;
- portfolio assets missing from the price history.
- empty uploads;
- wrong uploaded file type;
- duplicated portfolio assets.

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
- upload summary and upload report endpoints;
- optional asset class handling and inference;
- scenario engine output;
- concentration and top position report fields.

## Known Warning

The test suite currently shows a dependency-level FastAPI/Starlette warning:

```text
StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
```

The warning does not affect Stage 2 local behavior. It should be revisited when the FastAPI/Starlette test client ecosystem settles or when moving to a pinned production dependency set.

## Limitations

- Included data is sample/synthetic.
- Historical metrics are backward-looking.
- VaR and CVaR do not predict future losses.
- Stress tests are deterministic simplified shocks.
- Asset class inference is a simple fallback.
- Upload provenance is filename-level metadata only.
- No full broker margin model is included.
- No liquidity liquidation model is included.
- No broker connection or order execution is included.
- The API does not provide investment advice.

## Next Stage

Next stage should focus on user-defined scenario inputs, richer error response objects, cleaner adapters for different market data sources, and optional report export.
