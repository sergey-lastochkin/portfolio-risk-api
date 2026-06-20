# Manual Run Checklist

Use this checklist before showing the project to someone or before a public push.

## 1. Open Project

```bash
cd /Users/sergeylastochkin/Documents/Codex/2026-06-18/limit/portfolio-risk-api
```

## 2. Activate Virtual Environment

```bash
source .venv/bin/activate
```

If `.venv` does not exist:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## 3. Run API

```bash
make api
```

The server should start on:

```text
http://127.0.0.1:8000
```

## 4. Open FastAPI Docs

Open:

```text
http://127.0.0.1:8000/docs
```

You should see the Portfolio Risk API Swagger page.

## 5. Check Health

In another terminal:

```bash
curl http://127.0.0.1:8000/health
```

Expected response:

```json
{"status":"ok"}
```

## 6. Check Metadata

```bash
curl http://127.0.0.1:8000/metadata
```

Expected response should include:

- project name;
- version;
- limitations;
- implemented endpoints.

## 7. Check Risk Summary

```bash
curl -X POST http://127.0.0.1:8000/risk/summary \
  -H "Content-Type: application/json" \
  -d '{"portfolio_path":"data/sample_portfolio.csv","prices_path":"data/sample_prices.csv"}'
```

Expected response should include:

- `portfolio_value`;
- `weights`;
- `annualized_volatility`;
- `max_drawdown`;
- `var_95`;
- `cvar_95`;
- `stress_tests`;
- `limitations`.

## 8. Check Risk Report

```bash
curl -X POST http://127.0.0.1:8000/risk/report \
  -H "Content-Type: application/json" \
  -d '{"portfolio_path":"data/sample_portfolio.csv","prices_path":"data/sample_prices.csv"}'
```

Expected response should include everything from summary plus:

- `correlation_matrix`;
- `notes`.

## 9. Stop Server

Press:

```text
Ctrl+C
```

## 10. Final Local Checks

```bash
make test
make lint
```

Both should pass before public push.
