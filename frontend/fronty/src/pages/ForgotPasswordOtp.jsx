import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import AuthLayout from "../components/AuthLayout";
import { apiJson, formatError } from "../api";

export default function ForgotPasswordOtp() {
  const navigate = useNavigate();
  const [email, setEmail] = useState(
    sessionStorage.getItem("forgot_password_email") || ""
  );
  const [otp, setOtp] = useState("");
  const [success, setSuccess] = useState("");
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  async function handleSubmit(event) {
    event.preventDefault();
    setError("");
    setSuccess("");

    if (!email.trim()) {
      setError("Please enter your email address.");
      return;
    }

    if (otp.trim().length !== 6 || !/^\d+$/.test(otp.trim())) {
      setError("Enter the 6-digit code sent to your email.");
      return;
    }

    setBusy(true);

    const result = await apiJson("/api/v1/auth/forgot-password/verify/", {
      method: "POST",
      body: JSON.stringify({ email: email.trim(), otp: otp.trim() }),
    });

    setBusy(false);

    if (!result.ok) {
      setError(formatError(result.data));
      return;
    }

    sessionStorage.setItem("reset_token", result.data.reset_token);
    sessionStorage.setItem("forgot_password_email", email.trim());
    setSuccess(result.data.message || "OTP verified successfully.");

    setTimeout(() => {
      navigate("/reset-password");
    }, 800);
  }

  return (
    <AuthLayout
      eyebrow="Security check"
      title="Verify your code"
      description="Enter the 6-digit code we sent to your email to continue with your password reset."
      sideTitle="Stay in control"
      sideText="Reset your password securely without leaving the flow. You can continue when the code matches the email you entered."
    >
      <form className="form-stack" onSubmit={handleSubmit}>
        <label>
          Email address
          <input type="email" value={email} onChange={(event) => setEmail(event.target.value)} placeholder="you@example.com" />
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
        {success && <p className="form-message form-message--success">{success}</p>}

        <button type="submit" className="button button--primary button--full" disabled={busy}>
          {busy ? "Verifying…" : "Verify code"}
        </button>

        <div className="aux-links">
          <Link to="/forgot-password">Back</Link>
          <Link to="/login">Login</Link>
        </div>
      </form>
    </AuthLayout>
  );
}
