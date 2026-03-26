export default function KPI({ label, value }) {
  return (
    <div className="kpi-card">
      <p>{label}</p>
      <h3>{value}</h3>
    </div>
  );
}
