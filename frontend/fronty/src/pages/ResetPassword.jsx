import { useState } from "react";
import { Link } from "react-router-dom";
import AuthLayout from "../components/AuthLayout";
import { apiJson, formatError } from "../api";

export default function ResetPassword() {
  const [email] = useState(
    sessionStorage.getItem("forgot_password_email") || ""
  );
  const [resetToken] = useState(
    sessionStorage.getItem("reset_token") || ""
  );
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  async function handleSubmit(event) {
    event.preventDefault();

    if (!resetToken) {
      setError("No reset token is available. Please complete OTP verification first.");
      setMessage("");
      return;
    }

    if (password.length < 8) {
      setError("Your password should be at least 8 characters long.");
      setMessage("");
      return;
    }

    if (password !== confirmPassword) {
      setError("Passwords do not match.");
      setMessage("");
      return;
    }

    setError("");
    setMessage("");
    setBusy(true);

    const result = await apiJson("/api/v1/auth/forgot-password/reset/", {
      method: "POST",
      body: JSON.stringify({
        email,
        reset_token: resetToken,
        new_password: password,
      }),
    });

    setBusy(false);

    if (!result.ok) {
      setError(formatError(result.data));
      return;
    }

    sessionStorage.removeItem("reset_token");
    sessionStorage.removeItem("forgot_password_email");
    setMessage(result.data.message || "Password reset successfully.");
  }

  return (
    <AuthLayout
      eyebrow="New password"
      title="Choose a secure password"
      description="Create a new password for your account and sign in again."
      sideTitle="Protected access"
      sideText="A strong password helps keep your conversations, profile, and personal data secure."
    >
      <form className="form-stack" onSubmit={handleSubmit}>
        <label>
          New password
          <input type="password" value={password} onChange={(event) => setPassword(event.target.value)} placeholder="At least 8 characters" />
        </label>

        <label>
          Confirm password
          <input type="password" value={confirmPassword} onChange={(event) => setConfirmPassword(event.target.value)} placeholder="Repeat your password" />
        </label>

        {error && <p className="form-message form-message--error">{error}</p>}
        {message && <p className="form-message form-message--success">{message}</p>}

        <button type="submit" className="button button--primary button--full" disabled={busy}>
          {busy ? "Updating…" : "Update password"}
        </button>

        <div className="aux-links">
          <Link to="/login">Back to login</Link>
        </div>
      </form>
    </AuthLayout>
  );
}
