# GitHub Publication Notes

Use this file when preparing Portfolio Risk API for public GitHub release.

## Repository Description

```text
Reusable portfolio risk backend with FastAPI, CSV inputs, VaR/CVaR, drawdown, stress tests, Docker, and documented methodology.
```

## Topics

```text
portfolio-risk
risk-management
fastapi
python
var
cvar
drawdown
stress-testing
financial-engineering
quantitative-finance
```

## Short Tagline

```text
Reusable FastAPI backend for portfolio risk calculations from CSV data.
```

## Long Project Summary

Portfolio Risk API is a small backend service for calculating first-pass portfolio risk metrics from simple CSV inputs. It accepts a portfolio file and historical price file, validates the inputs, calculates weights and historical risk metrics, and returns JSON summaries or reports through FastAPI endpoints.

The project is intentionally narrow at Stage 2 local. It focuses on clean data validation, transparent methodology, tests, upload support, richer risk reports, and documented limitations. It does not provide investment advice, trading signals, broker connectivity, or live trading functionality.

## What To Show In A Pinned Repository

- Clear README with purpose and limitations.
- FastAPI endpoints.
- Sample CSV inputs.
- Methodology docs.
- Test coverage for risk metrics and validation.
- Dockerfile.
- Public push checklist.

## What Not To Claim

- No alpha.
- No trading signals.
- No arbitrage.
- No profit.
- No investment advice.
- No full portfolio management system.
- No live broker integration.
- No prediction of future losses.
- No claim that Stage 2 is a complete risk platform.

## Pre-Push Checklist

- [ ] Fresh owner review.
- [ ] `README.md` checked.
- [ ] `docs/project_status.md` checked.
- [ ] `docs/public_push_checklist.md` checked.
- [ ] No secrets or `.env`.
- [ ] No real client data.
- [ ] Sample data clearly marked as sample/synthetic.
- [ ] `python -m compileall src tests` passed.
- [ ] `pytest -q` passed.
- [ ] `ruff check .` passed.
- [ ] `black --check .` passed.
- [ ] `make test` passed.
- [ ] `make lint` passed.
- [ ] Docker build checked.
- [ ] Docker health checked.

## Post-Push Checklist

- [ ] GitHub README renders correctly.
- [ ] Repository description is set.
- [ ] Topics are set.
- [ ] No unwanted files are visible.
- [ ] Clone/install instructions work on a fresh checkout.
- [ ] Pinned repository order is intentional.
- [ ] Portfolio strategy text stays honest: this is Stage 2 local, not a full risk platform.
