from datetime import datetime
from pydantic import BaseModel
from uuid import UUID


class ScanRunOut(BaseModel):
    id: UUID
    tool: str
    status: str
    started_at: datetime
    finished_at: datetime | None

    class Config:
        from_attributes = True


class FindingOut(BaseModel):
    id: UUID
    title: str
    severity: str
    tool: str
    category: str | None
    service: str | None
    canonical_resource_id: str | None
    status: str

    class Config:
        from_attributes = True


class AlertOut(BaseModel):
    id: UUID
    severity: str
    message: str
    event_type: str
    occurred_at: datetime
    source_tool: str

    class Config:
        from_attributes = True


class ResourceOut(BaseModel):
    id: UUID
    name: str
    type: str
    provider: str
    region: str | None

    class Config:
        from_attributes = True


class Paginated(BaseModel):
    items: list


class SeverityBreakdown(BaseModel):
    total: int
    by_severity: dict[str, int]


class AIRequest(BaseModel):
    finding_id: UUID | None = None
    cve_id: str | None = None


class AIResponse(BaseModel):
    session_id: str
    audit_id: str
    response: dict
