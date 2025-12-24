import { useQuery } from '@tanstack/react-query';
import { listAlerts } from '../lib/api';

export default function Alerts() {
  const { data } = useQuery({ queryKey: ['alerts'], queryFn: listAlerts });

  return (
    <div className="space-y-4">
      <h1>Alerts</h1>
      <div className="bg-white rounded-lg shadow-sm overflow-hidden">
        <table className="min-w-full text-sm">
          <thead className="bg-slate-100 text-left">
            <tr>
              <th className="px-4 py-2">Severity</th>
              <th className="px-4 py-2">Type</th>
              <th className="px-4 py-2">Message</th>
              <th className="px-4 py-2">Occurred</th>
            </tr>
          </thead>
          <tbody>
            {data?.map((alert) => (
              <tr key={alert.id} className="border-t">
                <td className="px-4 py-2 capitalize">{alert.severity}</td>
                <td className="px-4 py-2">{alert.event_type}</td>
                <td className="px-4 py-2">{alert.message}</td>
                <td className="px-4 py-2">{new Date(alert.occurred_at).toLocaleString()}</td>
              </tr>
            ))}
            {data?.length === 0 && (
              <tr>
                <td className="px-4 py-4 text-center text-slate-500" colSpan={4}>
                  No alerts yet.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
