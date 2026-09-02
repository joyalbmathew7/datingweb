import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { verifyEmail } from "../services/auth";

function VerifyEmail() {
    const [email, setEmail] = useState("");
    const [otp, setOtp] = useState("");

    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);

    const navigate = useNavigate();

    async function handleSubmit(event) {
        event.preventDefault();

        setError("");
        setLoading(true);

        try {
            await verifyEmail({
                email,
                otp,
            });

            navigate("/login");
        } catch (error) {
            console.log("Verification failed:", error);
            setError(JSON.stringify(error));
        } finally {
            setLoading(false);
        }
    }

    return (
        <div>
            <h1>Verify Your Email</h1>

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
                    <label>Verification Code</label>

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
                    {loading ? "Verifying..." : "Verify Email"}
                </button>
            </form>
        </div>
    );
}

export default VerifyEmail;
