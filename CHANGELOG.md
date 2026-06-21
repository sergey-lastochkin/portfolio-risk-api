# Changelog

## 0.2.0 - Stage 2 local

- Added multipart CSV upload endpoints for risk summary and risk report.
- Added optional `asset_class` support with simple asset class inference.
- Added deterministic scenario engine.
- Expanded risk report with concentration, top positions, largest notional contributors, coverage, and provenance metadata.
- Strengthened validation for empty uploads, wrong file type, duplicated assets, and upload CSV errors.
- Added upload, scenario, concentration, and asset-class tests.
- Updated methodology, API design, limitations, and project status docs.

## 0.1.0 - Stage 1 MVP

- Initial FastAPI service.
- CSV sample inputs.
- Portfolio value and asset weights.
- Daily returns and portfolio returns.
- Annualized volatility and maximum drawdown.
- Historical VaR and CVaR as positive loss numbers.
- Correlation matrix.
- Simple stress tests.
- Dockerfile.
- Tests and methodology docs.
