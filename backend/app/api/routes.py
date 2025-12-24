from datetime import datetime
from uuid import uuid4

from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session

import redis.asyncio as redis

from backend.app.core.config import get_settings
from backend.app.db.session import SessionLocal
from backend.app.models import models
from backend.app.schemas.schemas import AlertOut, FindingOut, Paginated, ResourceOut, ScanRunOut
from backend.app.services.events import publish_alert_event, publish_scan_event
from backend.app.services.tasks import enqueue_fixture_scan

settings = get_settings()
router = APIRouter(prefix='/api')


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get('/health')
async def health():
    return {'status': 'ok'}


@router.get('/summary')
async def summary(db: Session = Depends(get_db)):
    findings = db.query(models.Finding).count()
    resources = db.query(models.Resource).count()
    alerts = db.query(models.Alert).count()
    scans = db.query(models.ScanRun).count()
    return {'findings': findings, 'resources': resources, 'alerts': alerts, 'scans': scans}


@router.get('/findings', response_model=Paginated)
async def list_findings(db: Session = Depends(get_db)):
    items = db.query(models.Finding).order_by(models.Finding.first_seen.desc()).all()
    payload = [
        FindingOut(
            id=f.id,
            title=f.title,
            severity=f.severity,
            tool=f.tool,
            category=f.category,
            service=f.service,
            canonical_resource_id=f.canonical_resource_id,
            status=f.status,
        )
        for f in items
    ]
    return {'items': payload}


@router.get('/scans', response_model=Paginated)
async def list_scans(db: Session = Depends(get_db)):
    items = db.query(models.ScanRun).order_by(models.ScanRun.started_at.desc()).all()
    payload = [
        ScanRunOut(
            id=s.id,
            tool=s.tool,
            status=s.status,
            started_at=s.started_at,
            finished_at=s.finished_at,
        )
        for s in items
    ]
    return {'items': payload}


@router.post('/scans', response_model=ScanRunOut)
async def create_scan(body: dict, db: Session = Depends(get_db)):
    tool = body.get('tool') or 'prowler'
    fixture = body.get('fixture', False)
    scan = models.ScanRun(id=uuid4(), tool=tool, status='queued', scope_json={'fixture': fixture})
    db.add(scan)
    db.commit()
    db.refresh(scan)
    publish_scan_event({'scan_id': str(scan.id), 'status': 'queued', 'tool': scan.tool})
    enqueue_fixture_scan(str(scan.id))
    return ScanRunOut.from_orm(scan)


@router.get('/alerts', response_model=Paginated)
async def list_alerts(db: Session = Depends(get_db)):
    items = db.query(models.Alert).order_by(models.Alert.occurred_at.desc()).all()
    payload = [
        AlertOut(
            id=a.id,
            severity=a.severity,
            message=a.message,
            event_type=a.event_type,
            occurred_at=a.occurred_at,
            source_tool=a.source_tool,
        )
        for a in items
    ]
    return {'items': payload}


@router.post('/alerts')
async def ingest_alert(alert: dict, db: Session = Depends(get_db)):
    item = models.Alert(
        id=uuid4(),
        source_tool=alert.get('source_tool', 'falco'),
        severity=alert.get('severity', 'info'),
        message=alert.get('message', ''),
        event_type=alert.get('event_type', 'runtime'),
        event_json=alert,
        occurred_at=datetime.utcnow(),
    )
    db.add(item)
    db.commit()
    publish_alert_event({
        'id': str(item.id),
        'severity': item.severity,
        'message': item.message,
        'event_type': item.event_type,
        'occurred_at': item.occurred_at.isoformat(),
        'source_tool': item.source_tool,
    })
    return {'id': str(item.id)}


@router.get('/resources', response_model=Paginated)
async def list_resources(db: Session = Depends(get_db)):
    items = db.query(models.Resource).all()
    payload = [
        ResourceOut(id=r.id, name=r.name, type=r.type, provider=r.provider, region=r.region) for r in items
    ]
    return {'items': payload}


@router.websocket('/ws/scans')
async def scan_updates(websocket: WebSocket):
    await websocket.accept()
    client = redis.from_url(settings.redis_url, decode_responses=True)
    pubsub = client.pubsub()
    await pubsub.subscribe('scans')
    try:
        async for message in pubsub.listen():
            if message['type'] == 'message':
                await websocket.send_text(message['data'])
    except WebSocketDisconnect:
        await websocket.close()
    finally:
        await pubsub.unsubscribe('scans')
        await client.aclose()


@router.websocket('/ws/alerts')
async def alert_updates(websocket: WebSocket):
    await websocket.accept()
    client = redis.from_url(settings.redis_url, decode_responses=True)
    pubsub = client.pubsub()
    await pubsub.subscribe('alerts')
    try:
        async for message in pubsub.listen():
            if message['type'] == 'message':
                await websocket.send_text(message['data'])
    except WebSocketDisconnect:
        await websocket.close()
    finally:
        await pubsub.unsubscribe('alerts')
        await client.aclose()
