# Aura Guard Runbook

## Prerequisites
- Docker and Docker Compose
- Node.js 18+ for local frontend dev (optional)

## Quickstart
1. Copy `.env.example` to `.env` and adjust if needed.
2. Run database migrations and start stack:
```bash
docker compose up --build
```
3. Frontend available at http://localhost:4173, backend at http://localhost:8000/api.
   - Celery worker is started by compose and processes fixture scans asynchronously via Redis.
   - WebSocket endpoints for scan and alert streaming: `ws://localhost:8000/api/ws/scans` and `ws://localhost:8000/api/ws/alerts`.

### Using the upstream Aura Guard frontend
If you want to run the UI from https://github.com/sidpan89/aura-guard instead of the in-repo frontend, fetch it and point the compose service at it:

```bash
make fetch-frontend   # or bash scripts/fetch_external_frontend.sh
echo "FRONTEND_DIR=external/aura-guard" >> .env
docker compose up --build frontend
```
The compose frontend container will `cd $FRONTEND_DIR` before installing dependencies and starting Vite, so the external UI will be served on port 4173.

## Local Backend Dev
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
alembic -c backend/alembic.ini upgrade head
uvicorn backend.app.main:app --reload
```

## Trigger Fixture Scan
Use UI Scans page or:
```bash
curl -X POST http://localhost:8000/api/scans -H 'Content-Type: application/json' -d '{"tool":"prowler","fixture":true}'
```
This enqueues a Celery task; monitor scan events over the scans WebSocket channel.

## Ingest Falco Alert
```bash
curl -X POST http://localhost:8000/api/alerts -H 'Content-Type: application/json' -d @fixtures/falco/sample.json
```

## Exercise AI helpers (stubbed)
```bash
# Replace <finding_uuid> with a known finding id from the database
curl -X POST http://localhost:8000/api/ai/explain -H 'Content-Type: application/json' -d '{"finding_id":"<finding_uuid>"}'
curl -X POST http://localhost:8000/api/ai/correlate -H 'Content-Type: application/json' -d '{"finding_id":"<finding_uuid>"}'
curl -X POST http://localhost:8000/api/ai/remediation -H 'Content-Type: application/json' -d '{"finding_id":"<finding_uuid>"}'
curl -X POST http://localhost:8000/api/ai/investigate -H 'Content-Type: application/json' -d '{"cve_id":"CVE-2023-0001"}'
```
