export type Severity = 'critical' | 'high' | 'medium' | 'low' | 'info';

export interface Finding {
  id: number;
  title: string;
  severity: Severity;
  tool: string;
  category: string;
  service: string;
  resource_name: string;
  canonical_resource_id: string;
  status: string;
}

export interface ScanRun {
  id: number;
  tool: string;
  status: string;
  started_at: string;
  finished_at?: string;
}

export interface AlertEvent {
  id: number;
  severity: Severity;
  message: string;
  event_type: string;
  occurred_at: string;
  source_tool: string;
}

export interface Resource {
  id: number;
  name: string;
  type: string;
  provider: string;
  region: string;
}
