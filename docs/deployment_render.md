# Deploying to Render

## Overview

Portfolio Risk API can run on Render as a public Docker web service. The hosted service uses the same FastAPI application and sample data as the local project.

The deployment was verified on June 21, 2026:

- Service: `portfolio-risk-api`
- URL: https://portfolio-risk-api-eb40.onrender.com
- Plan: Free
- Runtime: Docker
- Branch: `main`
- Health check: `/health`
- User-configured environment variables: none

Live verification results:

- `GET /health`: `200`, `{"status":"ok"}`
- `GET /metadata`: `200`, version `0.2.0`
- `GET /docs`: `200`
- `scripts/smoke_render.sh`: passed
- Render runtime log: Uvicorn bound to `0.0.0.0:10000`; health checks returned `200`

## Requirements

- Public GitHub repository: `sergey-lastochkin/portfolio-risk-api`
- Branch: `main`
- Runtime: Docker
- Health check path: `/health`
- No secrets, API keys, database, or broker credentials are required

## Docker and Runtime Notes

The Docker image starts Uvicorn on host `0.0.0.0`. It reads the `PORT` environment variable supplied by Render and falls back to `8000` locally.

Render sets its hosted-environment marker automatically. In that environment, server-side path endpoints are disabled because public clients must not select files from the service filesystem. Use these multipart endpoints instead:

- `POST /risk/summary/upload`
- `POST /risk/report/upload`

Local and trusted environments retain the path-based endpoints.

## Manual Render Dashboard Deployment

1. Open Render Dashboard.
2. Select **New**, then **Web Service**.
3. Connect GitHub repository `sergey-lastochkin/portfolio-risk-api`.
4. Select branch `main`.
5. Select the Docker runtime so Render uses the repository `Dockerfile`.
6. Set the health check path to `/health`.
7. Leave secrets and custom environment variables empty for the MVP.
8. Deploy the service.
9. After deployment, open `/health`, `/metadata`, and `/docs` on the assigned Render URL.

No `render.yaml` is required for this manual setup.

## Port Binding

The production command is equivalent to:

```bash
uvicorn portfolio_risk_api.app:app --host 0.0.0.0 --port "${PORT:-8000}"
```

Do not replace `0.0.0.0` with `127.0.0.1` in the container.

## Smoke Tests

Use the deployed service URL:

```bash
curl https://portfolio-risk-api-eb40.onrender.com/health
curl https://portfolio-risk-api-eb40.onrender.com/metadata
```

Or run:

```bash
./scripts/smoke_render.sh https://portfolio-risk-api-eb40.onrender.com
```

Expected health response:

```json
{"status":"ok"}
```

Use Swagger UI at `/docs` to test multipart CSV uploads with the included sample files.

## Environment Variables

No user-configured environment variables are required for the MVP. Render supplies `PORT` and its hosted-environment marker automatically. No secrets should be added.

## Common Failure Cases

- **Service cannot bind:** confirm the Docker command uses `0.0.0.0` and `${PORT:-8000}`.
- **Health check fails:** confirm the health path is exactly `/health` and inspect Render build/runtime logs.
- **Path endpoint returns 403:** expected on Render; use an `/upload` endpoint.
- **Upload returns 400:** confirm both files are non-empty CSV files with the documented columns.
- **Upload returns 422:** confirm both multipart fields are present and `var_level` remains `0.95`.
- **Slow first request:** free hosted services may need time to wake after inactivity.

## Limitations

- Included data is sample/synthetic.
- Historical risk metrics are backward-looking.
- Stress scenarios are deterministic diagnostics, not forecasts.
- The service has no broker connection or order execution.
- The service does not provide investment advice or trading recommendations.
- Availability and resource limits depend on the selected Render service plan.
