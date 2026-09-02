import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import AuthLayout from "../components/AuthLayout";
import { apiJson, formatError } from "../api";

export default function Register() {
  const navigate = useNavigate();
  const [form, setForm] = useState({
    username: "",
    email: "",
    password: "",
  });
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  function handleChange(event) {
    const { name, value } = event.target;
    setForm((current) => ({ ...current, [name]: value }));
  }

  async function handleSubmit(event) {
    event.preventDefault();
    setError("");
    setMessage("");
    setBusy(true);

    const result = await apiJson("/api/v1/auth/register/", {
      method: "POST",
      body: JSON.stringify({
        username: form.username.trim(),
        email: form.email.trim(),
        password: form.password,
      }),
    });

    setBusy(false);

    if (!result.ok) {
      setError(formatError(result.data));
      return;
    }

    sessionStorage.setItem("pending_verify_email", form.email.trim());
    setMessage("Registration successful. Please verify your email to continue.");

    setTimeout(() => {
      navigate("/verify-email");
    }, 1000);
  }

  return (
    <AuthLayout
      eyebrow="Create account"
      title="Join Kindred"
      description="Start with a few details and get ready to discover your next meaningful connection."
      sideTitle="Thoughtful introductions"
      sideText="You create a profile, verify your email, and begin connecting with people who match your pace and values."
    >
      <form className="form-stack" onSubmit={handleSubmit}>
        <label>
          Username
          <input name="username" value={form.username} onChange={handleChange} placeholder="Choose a username" />
        </label>

        <label>
          Email
          <input type="email" name="email" value={form.email} onChange={handleChange} placeholder="you@example.com" />
        </label>

        <label>
          Password
          <input type="password" name="password" value={form.password} onChange={handleChange} placeholder="Create a password" />
        </label>

        {error && <p className="form-message form-message--error">{error}</p>}
        {message && <p className="form-message form-message--success">{message}</p>}

        <button type="submit" className="button button--primary button--full" disabled={busy}>
          {busy ? "Creating…" : "Create account"}
        </button>

        <div className="aux-links">
          <Link to="/login">Already have an account?</Link>
        </div>
      </form>
    </AuthLayout>
  );
}
