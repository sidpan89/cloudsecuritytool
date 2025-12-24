"""Deterministic AI orchestration stubs used for local development.

These helpers keep all processing offline while still emitting audit and
session records to mirror how the real assistant flow will behave.
"""

from typing import Any, Dict
from uuid import UUID

from sqlalchemy.orm import Session

from backend.app import models


def _record_session(
    db: Session, kind: str, request: Dict[str, Any], response: Dict[str, Any]
):
    session = models.AISession(kind=kind, request_json=request, response_json=response)
    audit = models.AuditLog(
        actor="system",
        action=f"ai_{kind}",
        target_type="ai_session",
        target_id=None,
        payload_json={"request": request, "response": response},
    )
    db.add(session)
    db.add(audit)
    db.commit()
    db.refresh(session)
    db.refresh(audit)
    return session, audit


def explain_finding(db: Session, finding_id: UUID):
    finding = db.query(models.Finding).get(finding_id)
    if not finding:
        return None
    response = {
        "summary": f"Finding '{finding.title}' explains a {finding.severity} risk in {finding.service or 'unknown service'}.",
        "recommendation": "Review misconfiguration, apply least privilege, and re-run scan after remediation.",
        "references": finding.references_json or [],
    }
    session, audit = _record_session(
        db,
        "explain_finding",
        {"finding_id": str(finding_id)},
        response,
    )
    return {
        "session_id": str(session.id),
        "audit_id": str(audit.id),
        "finding_id": str(finding_id),
        "response": response,
    }


def correlate_finding(db: Session, finding_id: UUID):
    finding = db.query(models.Finding).get(finding_id)
    if not finding:
        return None
    related = (
        db.query(models.Finding)
        .filter(models.Finding.canonical_resource_id == finding.canonical_resource_id)
        .limit(5)
        .all()
    )
    correlations = [
        {
            "id": str(f.id),
            "title": f.title,
            "severity": f.severity,
            "tool": f.tool,
        }
        for f in related
    ]
    response = {
        "resource": finding.canonical_resource_id,
        "related_findings": correlations,
        "note": "Correlated findings share the same resource identifier.",
    }
    session, audit = _record_session(
        db,
        "correlate_finding",
        {"finding_id": str(finding_id)},
        response,
    )
    return {
        "session_id": str(session.id),
        "audit_id": str(audit.id),
        "finding_id": str(finding_id),
        "response": response,
    }


def investigate_cve(db: Session, cve_id: str):
    response = {
        "cve": cve_id,
        "impact": "Stub analysis: CVE impact and potential blast radius.",
        "next_steps": ["Check affected packages", "Validate runtime exposure", "Plan patch rollout"],
    }
    session, audit = _record_session(
        db,
        "investigate_cve",
        {"cve_id": cve_id},
        response,
    )
    return {
        "session_id": str(session.id),
        "audit_id": str(audit.id),
        "cve_id": cve_id,
        "response": response,
    }


def remediation_plan(db: Session, finding_id: UUID):
    finding = db.query(models.Finding).get(finding_id)
    if not finding:
        return None
    response = {
        "cli": f"# review and apply manually\nremediate --resource {finding.canonical_resource_id} --rule {finding.rule_id or 'N/A'}",
        "terraform_patch": "# terraform patch stub\n# add least privilege policy change here",
        "custodian": {
            "policies": [
                {
                    "name": "demo-remediation-plan",
                    "resource": finding.service or "aws.resource",
                    "actions": ["notify", "mark-for-op"],
                }
            ]
        },
    }
    session, audit = _record_session(
        db,
        "remediation_plan",
        {"finding_id": str(finding_id)},
        response,
    )
    return {
        "session_id": str(session.id),
        "audit_id": str(audit.id),
        "finding_id": str(finding_id),
        "response": response,
    }
