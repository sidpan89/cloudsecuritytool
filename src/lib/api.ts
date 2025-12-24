import axios from 'axios';
import { Finding, ScanRun, AlertEvent, Resource } from '../types';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api'
});

export async function fetchDashboardSummary() {
  const res = await api.get('/summary');
  return res.data as { findings: number; resources: number; alerts: number; scans: number };
}

export async function listFindings() {
  const res = await api.get('/findings');
  return res.data.items as Finding[];
}

export async function listScans() {
  const res = await api.get('/scans');
  return res.data.items as ScanRun[];
}

export async function createFixtureScan(tool: string) {
  const res = await api.post('/scans', { tool, fixture: true });
  return res.data as ScanRun;
}

export async function listAlerts() {
  const res = await api.get('/alerts');
  return res.data.items as AlertEvent[];
}

export async function listResources() {
  const res = await api.get('/resources');
  return res.data.items as Resource[];
}

export default api;
