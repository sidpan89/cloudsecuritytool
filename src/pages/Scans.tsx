import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { createFixtureScan, listScans } from '../lib/api';

const tools = ['prowler', 'trivy', 'checkov'];

export default function Scans() {
  const queryClient = useQueryClient();
  const { data } = useQuery({ queryKey: ['scans'], queryFn: listScans });
  const mutation = useMutation({
    mutationFn: (tool: string) => createFixtureScan(tool),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['scans'] })
  });

  return (
    <div className="space-y-4">
      <h1>Scans</h1>
      <div className="flex items-center space-x-2">
        {tools.map((tool) => (
          <button
            key={tool}
            onClick={() => mutation.mutate(tool)}
            className="px-3 py-2 rounded-md bg-slate-900 text-white hover:bg-slate-800"
          >
            Run {tool} fixture
          </button>
        ))}
      </div>
      <div className="bg-white rounded-lg shadow-sm overflow-hidden">
        <table className="min-w-full text-sm">
          <thead className="bg-slate-100 text-left">
            <tr>
              <th className="px-4 py-2">Tool</th>
              <th className="px-4 py-2">Status</th>
              <th className="px-4 py-2">Started</th>
              <th className="px-4 py-2">Finished</th>
            </tr>
          </thead>
          <tbody>
            {data?.map((scan) => (
              <tr key={scan.id} className="border-t">
                <td className="px-4 py-2">{scan.tool}</td>
                <td className="px-4 py-2 capitalize">{scan.status}</td>
                <td className="px-4 py-2">{new Date(scan.started_at).toLocaleString()}</td>
                <td className="px-4 py-2">{scan.finished_at ? new Date(scan.finished_at).toLocaleString() : '-'}</td>
              </tr>
            ))}
            {data?.length === 0 && (
              <tr>
                <td className="px-4 py-4 text-center text-slate-500" colSpan={4}>
                  No scans yet.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
