export default function VisitsMapPage() {
  const mapSrc = `https://www.google.com/maps?q=37.7749,-122.4194&z=12&output=embed`;

  return (
    <section>
      <h1>Field CRM - Visit Tracking</h1>
      <div className="card">
        <p>Map preview for geo-tagging integration (Google Maps embed placeholder).</p>
        <iframe title="google-map" src={mapSrc} width="100%" height="320" style={{ border: 0 }} loading="lazy" />
      </div>
    </section>
  );
}
