import uuid
from sqlalchemy import Column, String, DateTime, func, Integer, JSON, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from backend.app.db.session import Base


def uuid_pk():
    return Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)


class CloudAccount(Base):
    __tablename__ = 'cloud_account'
    id = uuid_pk()
    tenant_id = Column(String, nullable=False, default='demo')
    provider = Column(String, nullable=False)
    name = Column(String, nullable=False)
    config_json = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class ScanRun(Base):
    __tablename__ = 'scan_run'
    id = uuid_pk()
    tenant_id = Column(String, nullable=False, default='demo')
    tool = Column(String, nullable=False)
    provider = Column(String, nullable=True)
    scope_json = Column(JSON, nullable=True)
    status = Column(String, nullable=False, default='pending')
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    finished_at = Column(DateTime(timezone=True), nullable=True)
    artifact_prefix = Column(String, nullable=True)
    error = Column(Text, nullable=True)


class Artifact(Base):
    __tablename__ = 'artifact'
    id = uuid_pk()
    tenant_id = Column(String, nullable=False, default='demo')
    scan_run_id = Column(UUID(as_uuid=True), ForeignKey('scan_run.id'))
    tool = Column(String, nullable=False)
    kind = Column(String, nullable=False)
    object_uri = Column(String, nullable=False)
    sha256 = Column(String, nullable=True)
    size = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Resource(Base):
    __tablename__ = 'resource'
    id = uuid_pk()
    tenant_id = Column(String, nullable=False, default='demo')
    canonical_id = Column(String, nullable=False, unique=True)
    provider = Column(String, nullable=False)
    type = Column(String, nullable=False)
    name = Column(String, nullable=False)
    region = Column(String, nullable=True)
    account_id = Column(String, nullable=True)
    tags_json = Column(JSON, nullable=True)
    attributes_json = Column(JSON, nullable=True)
    first_seen = Column(DateTime(timezone=True), server_default=func.now())
    last_seen = Column(DateTime(timezone=True), server_default=func.now())


class Relationship(Base):
    __tablename__ = 'relationship'
    id = uuid_pk()
    tenant_id = Column(String, nullable=False, default='demo')
    src_resource_id = Column(UUID(as_uuid=True), ForeignKey('resource.id'))
    dst_resource_id = Column(UUID(as_uuid=True), ForeignKey('resource.id'))
    rel_type = Column(String, nullable=False)
    attributes_json = Column(JSON, nullable=True)
    first_seen = Column(DateTime(timezone=True), server_default=func.now())
    last_seen = Column(DateTime(timezone=True), server_default=func.now())


class Finding(Base):
    __tablename__ = 'finding'
    id = uuid_pk()
    tenant_id = Column(String, nullable=False, default='demo')
    scan_run_id = Column(UUID(as_uuid=True), ForeignKey('scan_run.id'))
    tool = Column(String, nullable=False)
    category = Column(String, nullable=True)
    rule_id = Column(String, nullable=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    severity = Column(String, nullable=False)
    provider = Column(String, nullable=True)
    service = Column(String, nullable=True)
    region = Column(String, nullable=True)
    canonical_resource_id = Column(String, nullable=True)
    evidence_json = Column(JSON, nullable=True)
    references_json = Column(JSON, nullable=True)
    remediation_json = Column(JSON, nullable=True)
    dedupe_key = Column(String, nullable=True)
    first_seen = Column(DateTime(timezone=True), server_default=func.now())
    last_seen = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(String, nullable=False, default='open')


class Alert(Base):
    __tablename__ = 'alert'
    id = uuid_pk()
    tenant_id = Column(String, nullable=False, default='demo')
    source_tool = Column(String, nullable=False)
    provider = Column(String, nullable=True)
    canonical_resource_id = Column(String, nullable=True)
    event_type = Column(String, nullable=False)
    severity = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    event_json = Column(JSON, nullable=True)
    occurred_at = Column(DateTime(timezone=True), server_default=func.now())


class AISession(Base):
    __tablename__ = 'ai_session'
    id = uuid_pk()
    tenant_id = Column(String, nullable=False, default='demo')
    user_id = Column(String, nullable=True)
    kind = Column(String, nullable=False)
    request_json = Column(JSON, nullable=True)
    response_json = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class RemediationAction(Base):
    __tablename__ = 'remediation_action'
    id = uuid_pk()
    tenant_id = Column(String, nullable=False, default='demo')
    finding_id = Column(UUID(as_uuid=True), ForeignKey('finding.id'))
    action_type = Column(String, nullable=False)
    plan_json = Column(JSON, nullable=True)
    apply_status = Column(String, nullable=True)
    applied_at = Column(DateTime(timezone=True), nullable=True)
    audit_log_id = Column(UUID(as_uuid=True), ForeignKey('audit_log.id'), nullable=True)


class AuditLog(Base):
    __tablename__ = 'audit_log'
    id = uuid_pk()
    tenant_id = Column(String, nullable=False, default='demo')
    actor = Column(String, nullable=False)
    action = Column(String, nullable=False)
    target_type = Column(String, nullable=True)
    target_id = Column(String, nullable=True)
    payload_json = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
