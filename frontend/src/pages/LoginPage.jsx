import { useState } from 'react';
import { login } from '../services/authService';

export default function LoginPage() {
  const [email, setEmail] = useState('admin@example.com');
  const [password, setPassword] = useState('Admin@123');
  const [msg, setMsg] = useState('');

  const onSubmit = async (e) => {
    e.preventDefault();
    try {
      await login(email, password);
      setMsg('Login successful. JWT stored in browser storage.');
    } catch {
      setMsg('Login failed.');
    }
  };

  return (
    <section>
      <h1>Login</h1>
      <form className="card" onSubmit={onSubmit}>
        <input value={email} onChange={(e) => setEmail(e.target.value)} placeholder="Email" />
        <input value={password} onChange={(e) => setPassword(e.target.value)} placeholder="Password" type="password" />
        <button type="submit">Login</button>
        {msg && <p>{msg}</p>}
      </form>
    </section>
  );
}
