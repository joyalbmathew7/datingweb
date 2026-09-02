import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import AuthLayout from "../components/AuthLayout";
import { apiJson, formatError } from "../api";

export default function VerifyEmail() {
  const [email, setEmail] = useState(
    sessionStorage.getItem("pending_verify_email") || ""
  );
  const [otp, setOtp] = useState("");
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    const storedEmail = sessionStorage.getItem("pending_verify_email");
    if (storedEmail) {
      setEmail(storedEmail);
    }
  }, []);

  async function handleSubmit(event) {
    event.preventDefault();

    if (!email.trim()) {
      setError("Please enter your email address.");
      setMessage("");
      return;
    }

    if (otp.trim().length !== 6 || !/^\d+$/.test(otp.trim())) {
      setError("Please enter the 6-digit verification code.");
      setMessage("");
      return;
    }

    setError("");
    setMessage("");
    setBusy(true);

    const result = await apiJson("/api/v1/auth/verify-email/", {
      method: "POST",
      body: JSON.stringify({ email: email.trim(), otp: otp.trim() }),
    });

    setBusy(false);

    if (!result.ok) {
      setError(formatError(result.data));
      return;
    }

    sessionStorage.removeItem("pending_verify_email");
    setMessage(result.data.message || "Email verified successfully.");
  }

  return (
    <AuthLayout
      eyebrow="Verify email"
      title="Check your inbox"
      description="Enter the 6-digit code we sent to your email to confirm your account."
      sideTitle="Start safe and secure"
      sideText="Your profile and matches wait for you once the email is verified. Explore with confidence and clarity."
    >
      <form className="form-stack" onSubmit={handleSubmit}>
        <label>
          Email
          <input
            type="email"
            value={email}
            onChange={(event) => setEmail(event.target.value)}
            placeholder="you@example.com"
          />
        </label>

        <label>
          Verification code
          <input
            type="text"
            inputMode="numeric"
            maxLength={6}
            value={otp}
            onChange={(event) => setOtp(event.target.value.replace(/\D/g, ""))}
            placeholder="123456"
          />
        </label>

        {error && <p className="form-message form-message--error">{error}</p>}
        {message && <p className="form-message form-message--success">{message}</p>}

        <button type="submit" className="button button--primary button--full" disabled={busy}>
          {busy ? "Verifying…" : "Verify email"}
        </button>

        <div className="aux-links">
          <Link to="/login">Back to login</Link>
          <Link to="/register">Create account</Link>
        </div>
      </form>
    </AuthLayout>
  );
}
