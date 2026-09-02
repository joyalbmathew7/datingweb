import { useEffect, useState } from "react";
import { getCurrentUser } from "../../accounts/services/auth";
import { useNavigate } from "react-router-dom";
import { logoutUser } from "../../accounts/services/auth";
function Home() {
    const [user, setUser] = useState(null);
    const [error, setError] = useState("");
    const navigate = useNavigate();
    
    useEffect(() => {
        async function loadUser() {
            try {
                const data = await getCurrentUser();
                setUser(data);
            } catch (error) {
                console.log("Failed to load user:", error);
                setError("Could not load your account.");
            }
        }

        loadUser();
    }, []);

    if (error) {
        return <p>{error}</p>;
    }

    if (!user) {
        return <p>Loading...</p>;
    }

    return (
        
        <div>
<button
    onClick={async () => {
        try {
            await logoutUser();
        } catch (error) {
            console.log("Logout failed:", error);
        }

        localStorage.removeItem("access");
        localStorage.removeItem("refresh");

        navigate("/login");
    }}
>
    Logout
</button>

            <h1>Welcome, {user.username}!</h1>

            <p>Email: {user.email}</p>

            <p>You are logged in successfully.</p>
        </div>
    );
}

export default Home;
