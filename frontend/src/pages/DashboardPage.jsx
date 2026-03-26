import KPI from '../components/KPI';
import useAsync from '../hooks/useAsync';
import { getSalesSummary } from '../services/crmService';

export default function DashboardPage() {
  const { data, loading } = useAsync(getSalesSummary, []);

  return (
    <section>
      <h1>Dashboard</h1>
      {loading ? (
        <p>Loading summary...</p>
      ) : (
        <div className="kpi-grid">
          <KPI label="Orders" value={data?.orders_count ?? 0} />
          <KPI label="Booked Revenue" value={data?.booked_revenue ?? 0} />
          <KPI label="Received" value={data?.received_amount ?? 0} />
        </div>
      )}
    </section>
  );
}
