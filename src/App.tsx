import { Navigate, Route, Routes } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import Findings from './pages/Findings';
import Scans from './pages/Scans';
import Alerts from './pages/Alerts';
import Resources from './pages/Resources';
import Layout from './components/Layout';

function App() {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<Navigate to="/dashboard" />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/findings" element={<Findings />} />
        <Route path="/scans" element={<Scans />} />
        <Route path="/alerts" element={<Alerts />} />
        <Route path="/resources" element={<Resources />} />
      </Routes>
    </Layout>
  );
}

export default App;
