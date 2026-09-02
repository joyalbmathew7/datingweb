import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import AuthLayout from "../components/AuthLayout";
import { apiJson, formatError } from "../api";

export default function ForgotPassword() {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  async function handleSubmit(event) {
    event.preventDefault();
    setError("");
    setMessage("");
    setBusy(true);

    const result = await apiJson("/api/v1/auth/forgot-password/", {
      method: "POST",
      body: JSON.stringify({ email: email.trim() }),
    });

    setBusy(false);

    if (!result.ok) {
      setError(formatError(result.data));
      return;
    }

    sessionStorage.setItem("forgot_password_email", email.trim());
    setMessage(result.data.message || "A reset code has been sent.");

    setTimeout(() => {
      navigate("/forgot-password/verify");
    }, 700);
  }

  return (
    <AuthLayout
      eyebrow="Forgot password"
      title="Reset your password"
      description="Enter the email address linked to your account and we will send a verification code."
      sideTitle="Keep it secure"
      sideText="A simple reset flow keeps your profile safe while making it easy to get back in quickly."
    >
      <form className="form-stack" onSubmit={handleSubmit}>
        <label>
          Email address
          <input type="email" value={email} onChange={(event) => setEmail(event.target.value)} placeholder="you@example.com" />
        </label>

        {error && <p className="form-message form-message--error">{error}</p>}
        {message && <p className="form-message form-message--info">{message}</p>}

        <button type="submit" className="button button--primary button--full" disabled={busy}>
          {busy ? "Sending…" : "Send OTP"}
        </button>

        <div className="aux-links">
          <Link to="/login">Back to login</Link>
          <Link to="/forgot-password/verify">Verify code</Link>
        </div>
      </form>
    </AuthLayout>
  );
}
