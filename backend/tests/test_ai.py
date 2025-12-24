from uuid import uuid4

from fastapi.testclient import TestClient

from backend.app.main import app
from backend.app.db.session import SessionLocal, Base, engine
from backend.app import models


client = TestClient(app)


def _seed_finding():
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    finding = models.Finding(
        id=uuid4(),
        tool="prowler",
        title="S3 bucket is public",
        severity="high",
        category="s3",
        service="s3",
        canonical_resource_id="arn:aws:s3:::demo",
    )
    session.add(finding)
    session.commit()
    session.refresh(finding)
    session.close()
    return finding.id


def test_ai_explain_creates_session():
    finding_id = _seed_finding()
    resp = client.post("/api/ai/explain", json={"finding_id": str(finding_id)})
    assert resp.status_code == 200
    body = resp.json()
    assert body["session_id"]
    assert body["audit_id"]
    assert body["response"]["summary"].startswith("Finding 'S3 bucket is public'")


def test_ai_correlate_uses_resource_scope():
    finding_id = _seed_finding()
    resp = client.post("/api/ai/correlate", json={"finding_id": str(finding_id)})
    assert resp.status_code == 200
    body = resp.json()
    assert body["response"]["related_findings"]

