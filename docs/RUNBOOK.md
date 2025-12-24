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

## Ingest Falco Alert
```bash
curl -X POST http://localhost:8000/api/alerts -H 'Content-Type: application/json' -d @fixtures/falco/sample.json
```
