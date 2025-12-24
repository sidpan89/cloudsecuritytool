import json
from pathlib import Path
from uuid import uuid4
from datetime import datetime
from sqlalchemy.orm import Session

from adapters.registry import ADAPTERS
from backend.app.models import models
from backend.app.services.events import publish_scan_event
from backend.app.services.utils import normalize_resource_id


def ingest_fixture(db: Session, scan_id: str):
    scan = db.query(models.ScanRun).get(scan_id)
    if not scan:
        return
    adapter = ADAPTERS.get(scan.tool)
    if not adapter:
        scan.status = 'error'
        scan.error = 'adapter not found'
        db.commit()
        publish_scan_event({'scan_id': scan_id, 'status': 'error', 'error': scan.error})
        return
    scan.status = 'running'
    scan.started_at = datetime.utcnow()
    db.commit()
    publish_scan_event({'scan_id': scan_id, 'status': 'running', 'tool': scan.tool})
    fixture_path = Path('fixtures') / scan.tool / 'sample.json'
    payload = json.loads(fixture_path.read_text())
    records = adapter.parse(payload)
    for record in records:
        normalized = adapter.normalize(record)
        finding = models.Finding(
            id=uuid4(),
            scan_run_id=scan.id,
            tool=scan.tool,
            title=normalized.get('title') or 'Finding',
            severity=normalized.get('severity', 'low'),
            category=normalized.get('category'),
            service=normalized.get('service'),
            canonical_resource_id=normalize_resource_id(normalized.get('canonical_resource_id', 'unknown')),
            status='open',
        )
        db.add(finding)
        resource = models.Resource(
            id=uuid4(),
            canonical_id=finding.canonical_resource_id,
            provider='aws',
            type=normalized.get('service') or 'resource',
            name=finding.canonical_resource_id,
            region='us-east-1',
        )
        db.merge(resource)
    scan.status = 'completed'
    scan.finished_at = datetime.utcnow()
    db.commit()
    publish_scan_event({
        'scan_id': scan_id,
        'status': 'completed',
        'tool': scan.tool,
        'finished_at': scan.finished_at.isoformat() if scan.finished_at else None,
    })
