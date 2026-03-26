import useAsync from '../hooks/useAsync';
import { getPipeline } from '../services/crmService';

export default function PipelinePage() {
  const { data, loading } = useAsync(getPipeline, []);

  if (loading) return <p>Loading pipeline...</p>;

  return (
    <section>
      <h1>Sales Pipeline</h1>
      <p>Lead Conversion: {data?.lead_conversion_rate ?? 0}%</p>
      <div className="kanban">
        {Object.entries(data?.pipeline || {}).map(([stage, stats]) => (
          <div key={stage} className="card">
            <h3>{stage}</h3>
            <p>Deals: {stats.deal_count}</p>
            <p>Value: {stats.total_value}</p>
          </div>
        ))}
      </div>
    </section>
  );
}
