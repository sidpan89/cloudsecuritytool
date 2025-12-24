import { Link, useLocation } from 'react-router-dom';
import { ReactNode } from 'react';
import { Shield, List, Activity, AlertTriangle, Server } from 'lucide-react';
import clsx from 'clsx';

const navItems = [
  { to: '/dashboard', label: 'Dashboard', icon: Shield },
  { to: '/findings', label: 'Findings', icon: List },
  { to: '/scans', label: 'Scans', icon: Activity },
  { to: '/alerts', label: 'Alerts', icon: AlertTriangle },
  { to: '/resources', label: 'Resources', icon: Server }
];

export default function Layout({ children }: { children: ReactNode }) {
  const location = useLocation();
  return (
    <div className="min-h-screen grid grid-cols-[220px_1fr]">
      <aside className="bg-slate-900 text-slate-100 p-4 space-y-4">
        <div className="flex items-center space-x-2 text-lg font-semibold">
          <Shield className="w-6 h-6" />
          <span>Aura Guard</span>
        </div>
        <nav className="space-y-2">
          {navItems.map((item) => {
            const Icon = item.icon;
            const active = location.pathname.startsWith(item.to);
            return (
              <Link
                key={item.to}
                to={item.to}
                className={clsx(
                  'flex items-center space-x-2 px-3 py-2 rounded-md hover:bg-slate-800',
                  active && 'bg-slate-800'
                )}
              >
                <Icon className="w-4 h-4" />
                <span>{item.label}</span>
              </Link>
            );
          })}
        </nav>
      </aside>
      <main className="p-6 space-y-6">{children}</main>
    </div>
  );
}
