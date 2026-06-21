# Current Portfolio Risk API Handoff

Timestamp: 2026-06-21 18:18 MSK

## Status

- Repo: project root
- Branch: `main`
- Remote: none
- Latest commit: `671dc46 Add upload support and scenario risk reports`
- Push status: local only

## Current Stage

Stage 2 local MVP.

Implemented:

- path-based CSV risk summary/report;
- multipart upload summary/report;
- richer report fields;
- deterministic scenario engine;
- optional `asset_class` with simple inference;
- tests and docs.

## Latest Known Checks

- Test suite documented as `31 passed`.
- Docker build/run and `/health` were OK in the latest production pass.
- Known dependency-level FastAPI/Starlette TestClient warning remains.

## Next

1. Run fresh checks before publishing.
2. Re-run Docker build and `/health`.
3. Read README and `docs/public_push_checklist.md`.
4. Create remote and push only after explicit owner approval.
