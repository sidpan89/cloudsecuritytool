import { useQuery } from '@tanstack/react-query';
import { listFindings } from '../lib/api';

export default function Findings() {
  const { data } = useQuery({ queryKey: ['findings'], queryFn: listFindings });

  return (
    <div className="space-y-4">
      <h1>Findings</h1>
      <div className="bg-white rounded-lg shadow-sm overflow-hidden">
        <table className="min-w-full text-sm">
          <thead className="bg-slate-100 text-left">
            <tr>
              <th className="px-4 py-2">Title</th>
              <th className="px-4 py-2">Severity</th>
              <th className="px-4 py-2">Service</th>
              <th className="px-4 py-2">Resource</th>
            </tr>
          </thead>
          <tbody>
            {data?.map((finding) => (
              <tr key={finding.id} className="border-t">
                <td className="px-4 py-2">{finding.title}</td>
                <td className="px-4 py-2 capitalize">{finding.severity}</td>
                <td className="px-4 py-2">{finding.service}</td>
                <td className="px-4 py-2">{finding.resource_name}</td>
              </tr>
            ))}
            {data?.length === 0 && (
              <tr>
                <td className="px-4 py-4 text-center text-slate-500" colSpan={4}>
                  No findings yet.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
