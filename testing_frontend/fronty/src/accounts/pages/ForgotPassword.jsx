import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { forgotPassword } from "../services/auth";

function ForgotPassword() {
    const [email, setEmail] = useState("");

    const [message, setMessage] = useState("");
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);

    const navigate = useNavigate();

    async function handleSubmit(event) {
        event.preventDefault();

        setMessage("");
        setError("");
        setLoading(true);

        try {
            const data = await forgotPassword({
                email,
            });

            setMessage(data.message);

            navigate("/verify-password-otp", {
                state: {
                    email: email,
                },
            });
        } catch (error) {
            console.log("Forgot password failed:", error);
            setError(JSON.stringify(error));
        } finally {
            setLoading(false);
        }
    }

    return (
        <div>
            <h1>Forgot Password</h1>

            <p>
                Enter your email address to receive a password reset OTP.
            </p>

            {message && <p>{message}</p>}
            {error && <p>{error}</p>}

            <form onSubmit={handleSubmit}>
                <div>
                    <label>Email</label>

                    <input
                        type="email"
                        value={email}
                        onChange={(event) =>
                            setEmail(event.target.value)
                        }
                    />
                </div>

                <button type="submit" disabled={loading}>
                    {loading ? "Sending..." : "Send OTP"}
                </button>
            </form>

            <br />

            <button
                type="button"
                onClick={() => navigate("/login")}
            >
                Back to Login
            </button>
        </div>
    );
}

export default ForgotPassword;
