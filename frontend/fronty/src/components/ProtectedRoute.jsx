import { Navigate, Outlet } from "react-router-dom";
import { useAuth } from "../AuthContext";

export function ProtectedRoute() {
  const { user, ready } = useAuth();

  if (!ready) {
    return (
      <div className="boot-screen">
        <div className="boot-mark">K</div>
        <p>Loading Kindred…</p>
      </div>
    );
  }

  if (!user) {
    return <Navigate to="/login" replace />;
  }

  return <Outlet />;
}

export function GuestRoute() {
  const { user, ready } = useAuth();

  if (!ready) {
    return (
      <div className="boot-screen">
        <div className="boot-mark">K</div>
        <p>Loading Kindred…</p>
      </div>
    );
  }

  if (user) {
    return <Navigate to="/discover" replace />;
  }

  return <Outlet />;
}

export function ProfileGate() {
  const { profile, ready } = useAuth();

  if (!ready) return null;

  if (!profile) {
    return <Navigate to="/onboarding" replace />;
  }

  return <Outlet />;
}
