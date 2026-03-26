import { useEffect, useState } from 'react';
import { createLead, getLeads } from '../services/crmService';

const defaultLead = {
  company_id: 1,
  branch_id: 1,
  department_id: 1,
  customer_name: '',
  email: '',
  phone: '',
  status: 'New'
};

export default function LeadsPage() {
  const [leads, setLeads] = useState([]);
  const [form, setForm] = useState(defaultLead);

  const load = async () => setLeads(await getLeads({ limit: 50 }));

  useEffect(() => {
    load();
  }, []);

  const submit = async (e) => {
    e.preventDefault();
    await createLead(form);
    setForm(defaultLead);
    load();
  };

  return (
    <section>
      <h1>Leads</h1>
      <form className="card" onSubmit={submit}>
        <input placeholder="Customer Name" value={form.customer_name} onChange={(e) => setForm({ ...form, customer_name: e.target.value })} />
        <input placeholder="Email" value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} />
        <input placeholder="Phone" value={form.phone} onChange={(e) => setForm({ ...form, phone: e.target.value })} />
        <button type="submit">Add Lead</button>
      </form>

      <table>
        <thead>
          <tr><th>Customer</th><th>Status</th><th>Email</th><th>Phone</th></tr>
        </thead>
        <tbody>
          {leads.map((lead) => (
            <tr key={lead.id}><td>{lead.customer_name}</td><td>{lead.status}</td><td>{lead.email}</td><td>{lead.phone}</td></tr>
          ))}
        </tbody>
      </table>
    </section>
  );
}
