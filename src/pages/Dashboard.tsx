import { useQuery } from '@tanstack/react-query';
import { fetchDashboardSummary } from '../lib/api';

export default function Dashboard() {
  const { data } = useQuery({ queryKey: ['summary'], queryFn: fetchDashboardSummary });

  const cards = [
    { label: 'Findings', value: data?.findings ?? 0 },
    { label: 'Resources', value: data?.resources ?? 0 },
    { label: 'Alerts', value: data?.alerts ?? 0 },
    { label: 'Scans', value: data?.scans ?? 0 }
  ];

  return (
    <div className="space-y-4">
      <h1>Dashboard</h1>
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {cards.map((card) => (
          <div key={card.label} className="bg-white shadow-sm rounded-lg p-4">
            <div className="text-sm text-slate-500">{card.label}</div>
            <div className="text-2xl font-bold">{card.value}</div>
          </div>
        ))}
      </div>
    </div>
  );
}
