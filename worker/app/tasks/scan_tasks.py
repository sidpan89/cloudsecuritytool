import pathlib
import sys

from worker.app.celery_app import celery_app

ROOT = pathlib.Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from backend.app.db.session import SessionLocal
from backend.app.services.ingest import ingest_fixture


@celery_app.task
def run_fixture_scan(scan_id: str):
    db = SessionLocal()
    try:
        ingest_fixture(db, scan_id)
    finally:
        db.close()
    return {'status': 'completed', 'scan_id': scan_id}
