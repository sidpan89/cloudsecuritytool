import { useQuery } from '@tanstack/react-query';
import { listResources } from '../lib/api';

export default function Resources() {
  const { data } = useQuery({ queryKey: ['resources'], queryFn: listResources });

  return (
    <div className="space-y-4">
      <h1>Resources</h1>
      <div className="bg-white rounded-lg shadow-sm overflow-hidden">
        <table className="min-w-full text-sm">
          <thead className="bg-slate-100 text-left">
            <tr>
              <th className="px-4 py-2">Name</th>
              <th className="px-4 py-2">Type</th>
              <th className="px-4 py-2">Provider</th>
              <th className="px-4 py-2">Region</th>
            </tr>
          </thead>
          <tbody>
            {data?.map((resource) => (
              <tr key={resource.id} className="border-t">
                <td className="px-4 py-2">{resource.name}</td>
                <td className="px-4 py-2">{resource.type}</td>
                <td className="px-4 py-2">{resource.provider}</td>
                <td className="px-4 py-2">{resource.region}</td>
              </tr>
            ))}
            {data?.length === 0 && (
              <tr>
                <td className="px-4 py-4 text-center text-slate-500" colSpan={4}>
                  No resources yet.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
