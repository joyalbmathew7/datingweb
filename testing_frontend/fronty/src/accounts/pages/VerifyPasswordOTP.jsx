import { useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { verifyPasswordOTP } from "../services/auth";

function VerifyPasswordOTP() {
    const location = useLocation();
    const navigate = useNavigate();

    const emailFromForgotPassword = location.state?.email || "";

    const [email, setEmail] = useState(emailFromForgotPassword);
    const [otp, setOtp] = useState("");

    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);

    async function handleSubmit(event) {
        event.preventDefault();

        setError("");
        setLoading(true);

        try {
            const data = await verifyPasswordOTP({
                email,
                otp,
            });

            navigate("/reset-password", {
                state: {
                    email: email,
                    resetToken: data.reset_token,
                },
            });
        } catch (error) {
            console.log("OTP verification failed:", error);
            setError(JSON.stringify(error));
        } finally {
            setLoading(false);
        }
    }

    return (
        <div>
            <h1>Verify OTP</h1>

            <p>
                Enter the OTP sent to your email.
            </p>

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

                <div>
                    <label>OTP</label>

                    <input
                        type="text"
                        value={otp}
                        onChange={(event) =>
                            setOtp(event.target.value)
                        }
                        maxLength="6"
                    />
                </div>

                <button type="submit" disabled={loading}>
                    {loading ? "Verifying..." : "Verify OTP"}
                </button>
            </form>
        </div>
    );
}

export default VerifyPasswordOTP;
