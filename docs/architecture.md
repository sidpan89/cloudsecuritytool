# Architecture Overview
- FastAPI backend providing `/api` routes for scans, findings, alerts, resources, and summary.
- Celery worker ready for asynchronous scans (stubbed fixture task).
- Postgres stores normalized entities; Redis backs Celery.
- MinIO, Neo4j placeholders via docker-compose; MinIO initialized with `auraguard` bucket.
- Frontend is Vite + React consuming the API.
