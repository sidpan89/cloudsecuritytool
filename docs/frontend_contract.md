# Frontend Contract

## Routes/Pages
- `/dashboard`: shows summary cards for findings, resources, alerts, scans using `fetchDashboardSummary`.
- `/findings`: table listing findings via `listFindings`.
- `/scans`: table of scans via `listScans` and buttons to trigger `createFixtureScan` for prowler, trivy, checkov.
- `/alerts`: table listing alerts via `listAlerts`.
- `/resources`: table listing resources via `listResources`.

## Network Calls
- `GET /api/summary` -> `{ findings: number, resources: number, alerts: number, scans: number }`
- `GET /api/findings` -> `{ items: Finding[] }`
- `GET /api/findings/summary` -> `{ total: number, by_severity: Record<string, number> }`
- `GET /api/scans` -> `{ items: ScanRun[] }`
- `POST /api/scans { tool: string, fixture: boolean }` -> `ScanRun`
- `GET /api/alerts` -> `{ items: AlertEvent[] }`
- `GET /api/resources` -> `{ items: Resource[] }`
- AI helpers (not currently used by UI but exposed for future flows):
  - `POST /api/ai/explain { finding_id }` -> AIResponse
  - `POST /api/ai/correlate { finding_id }` -> AIResponse
  - `POST /api/ai/investigate { cve_id }` -> AIResponse
  - `POST /api/ai/remediation { finding_id }` -> AIResponse

## Data Shapes
- `Finding`: `{ id, title, severity, tool, category, service, canonical_resource_id, status, resource_name (derived in UI from canonical id) }`
- `ScanRun`: `{ id, tool, status, started_at, finished_at }`
- `AlertEvent`: `{ id, severity, message, event_type, occurred_at, source_tool }`
- `Resource`: `{ id, name, type, provider, region }`

## WebSockets
- None currently used by the UI.
