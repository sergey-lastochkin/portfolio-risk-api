# Public Push Checklist

Use this before pushing Portfolio Risk API to GitHub.

## Content

- [ ] README checked
- [ ] Project purpose is clear
- [ ] Sample data is marked synthetic/example
- [ ] No investment advice wording
- [ ] No alpha, signals, arbitrage, profit, or prediction claims
- [ ] Limitations are visible
- [ ] Stage 2 roadmap is honest

## Security and Data

- [ ] No `.env`
- [ ] No secrets
- [ ] No real API keys
- [ ] No broker credentials
- [ ] No real client data
- [ ] No private paths in docs
- [ ] `.venv/` is ignored
- [ ] caches are ignored

## Checks

- [ ] `python -m compileall src tests`
- [ ] `pytest -q`
- [ ] `ruff check .`
- [ ] `black --check .`
- [ ] `make test`
- [ ] `make lint`
- [ ] Docker build checked
- [ ] Docker run checked

## GitHub Setup

- [ ] GitHub description prepared
- [ ] Topics prepared
- [ ] First public commit ready
- [ ] Remote added intentionally
- [ ] Push done only after final owner review

Suggested description:

```text
Reusable FastAPI backend for portfolio risk calculations from CSV data.
```

Suggested topics:

```text
python, fastapi, portfolio-risk, risk-management, var, cvar, finance, pandas, quantitative-finance, api
```
