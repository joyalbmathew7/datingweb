import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import AuthLayout from "../components/AuthLayout";
import { apiJson, formatError, setTokens } from "../api";

export default function Login() {
  const navigate = useNavigate();
  const [identifier, setIdentifier] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  async function handleSubmit(event) {
    event.preventDefault();
    setError("");
    setMessage("");
    setBusy(true);

    const result = await apiJson("/api/v1/auth/login/", {
      method: "POST",
      body: JSON.stringify({ identifier: identifier.trim(), password }),
    });

    setBusy(false);

    if (!result.ok) {
      setError(formatError(result.data));
      return;
    }

    setTokens(result.data.access, result.data.refresh);
    setMessage("Login successful. JWT tokens were saved locally.");

    setTimeout(() => {
      navigate("/");
    }, 800);
  }

  return (
    <AuthLayout
      eyebrow="Welcome back"
      title="Log in to Kindred"
      description="Use your email or username to continue your dating journey."
      sideTitle="Find your kind of connection"
      sideText="Explore thoughtful profiles, message matches, and build a stronger dating experience from the first hello."
    >
      <form className="form-stack" onSubmit={handleSubmit}>
        <label>
          Username or email
          <input
            value={identifier}
            onChange={(event) => setIdentifier(event.target.value)}
            autoComplete="username"
            placeholder="joyal@gmail.com"
          />
        </label>

        <label>
          Password
          <input
            type="password"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
            autoComplete="current-password"
            placeholder="Enter your password"
          />
        </label>

        {error && <p className="form-message form-message--error">{error}</p>}
        {message && <p className="form-message form-message--success">{message}</p>}

        <button type="submit" className="button button--primary button--full" disabled={busy}>
          {busy ? "Logging in…" : "Log in"}
        </button>

        <div className="aux-links">
          <Link to="/forgot-password">Forgot password?</Link>
          <Link to="/register">Create account</Link>
        </div>
      </form>
    </AuthLayout>
  );
}
