import {
    BrowserRouter,
    Routes,
    Route,
    Navigate,
} from "react-router-dom";

import Register from "./accounts/pages/Register";
import VerifyEmail from "./accounts/pages/VerifyEmail";
import Login from "./accounts/pages/Login";
import Home from "./homepage/pages/Home";
import ForgotPassword from "./accounts/pages/ForgotPassword";
import VerifyPasswordOTP from "./accounts/pages/VerifyPasswordOTP";
import ResetPassword from "./accounts/pages/ResetPassword";
import ProtectedRoute from "./accounts/components/ProtectedRoute";

function App() {
    return (
        <BrowserRouter>
            <Routes>
                <Route
                    path="/"
                    element={<Navigate to="/register" />}
                />

                <Route
                    path="/register"
                    element={<Register />}
                />

                <Route
                    path="/verify-email"
                    element={<VerifyEmail />}
                />

                <Route
                    path="/login"
                    element={<Login />}
                />

                <Route
                    path="/forgot-password"
                    element={<ForgotPassword />}
                />

                <Route
                    path="/home"
                    element={
                        <ProtectedRoute>
                            <Home />
                        </ProtectedRoute>
                    }
                />

                
                <Route
    path="/verify-password-otp"
    element={<VerifyPasswordOTP />}
/>
<Route
    path="/reset-password"
    element={<ResetPassword />}
/>
            </Routes>
        </BrowserRouter>
    );
}

export default App;