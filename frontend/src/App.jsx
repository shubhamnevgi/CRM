import { NavLink, Route, Routes } from 'react-router-dom';
import DashboardPage from './pages/DashboardPage';
import LeadsPage from './pages/LeadsPage';
import LoginPage from './pages/LoginPage';
import OrdersPage from './pages/OrdersPage';
import PipelinePage from './pages/PipelinePage';
import QuotationPage from './pages/QuotationPage';
import VisitsMapPage from './pages/VisitsMapPage';

const links = [
  ['/', 'Dashboard'],
  ['/leads', 'Leads'],
  ['/pipeline', 'Pipeline'],
  ['/quotations', 'Quotations'],
  ['/orders', 'Orders'],
  ['/visits', 'Visits Map'],
  ['/login', 'Login']
];

export default function App() {
  return (
    <div className="app-shell">
      <aside className="sidebar">
        <h2>CRM ERP</h2>
        {links.map(([to, label]) => (
          <NavLink key={to} to={to} className="nav-link">
            {label}
          </NavLink>
        ))}
      </aside>
      <main className="content">
        <Routes>
          <Route path="/" element={<DashboardPage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/leads" element={<LeadsPage />} />
          <Route path="/pipeline" element={<PipelinePage />} />
          <Route path="/quotations" element={<QuotationPage />} />
          <Route path="/orders" element={<OrdersPage />} />
          <Route path="/visits" element={<VisitsMapPage />} />
        </Routes>
      </main>
    </div>
  );
}
