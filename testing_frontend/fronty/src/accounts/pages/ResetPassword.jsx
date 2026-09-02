import { useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { resetPassword } from "../services/auth";

function ResetPassword() {
    const location = useLocation();
    const navigate = useNavigate();

    const email = location.state?.email || "";
    const resetToken = location.state?.resetToken || "";

    const [newPassword, setNewPassword] = useState("");
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);

    async function handleSubmit(event) {
        event.preventDefault();

        setError("");
        setLoading(true);

        try {
            await resetPassword({
                email,
                reset_token: resetToken,
                new_password: newPassword,
            });

            navigate("/login");
        } catch (error) {
            console.log("Password reset failed:", error);
            setError(JSON.stringify(error));
        } finally {
            setLoading(false);
        }
    }

    return (
        <div>
            <h1>Reset Password</h1>

            <p>Create a new password for your account.</p>

            {error && <p>{error}</p>}

            <form onSubmit={handleSubmit}>
                <div>
                    <label>New Password</label>

                    <input
                        type="password"
                        value={newPassword}
                        onChange={(event) =>
                            setNewPassword(event.target.value)
                        }
                    />
                </div>

                <button type="submit" disabled={loading}>
                    {loading ? "Resetting..." : "Reset Password"}
                </button>
            </form>
        </div>
    );
}

export default ResetPassword;
