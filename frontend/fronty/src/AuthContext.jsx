import { createContext, useContext, useEffect, useMemo, useState } from "react";
import { apiJson, clearTokens, setTokens } from "./api";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [profile, setProfile] = useState(null);
  const [ready, setReady] = useState(false);

  async function loadSession() {
    const me = await apiJson("/api/v1/auth/me/");
    if (!me.ok) {
      setUser(null);
      setProfile(null);
      setReady(true);
      return;
    }

    setUser(me.data);

    const mine = await apiJson("/api/v1/profiles/me/");
    if (mine.status === 404) {
      setProfile(null);
      setReady(true);
      return;
    }

    if (mine.ok) {
      setProfile(mine.data);
    } else {
      setProfile(null);
    }

    setReady(true);
  }

  useEffect(() => {
    loadSession();
  }, []);

  async function login(identifier, password) {
    const response = await apiJson("/api/v1/auth/login/", {
      method: "POST",
      body: JSON.stringify({ identifier, password }),
    });

    if (!response.ok) return response;

    setTokens(response.data.access, response.data.refresh);
    await loadSession();
    return response;
  }

  async function register(username, email, password) {
    const created = await apiJson("/api/v1/auth/register/", {
      method: "POST",
      body: JSON.stringify({ username, email, password }),
    });

    if (!created.ok) return created;
    return login(username, password);
  }

  async function logout() {
    const refresh = localStorage.getItem("kindred_refresh");
    if (refresh) {
      await apiJson("/api/v1/auth/logout/", {
        method: "POST",
        body: JSON.stringify({ refresh }),
      });
    }
    clearTokens();
    setUser(null);
    setProfile(null);
  }

  async function refreshProfile() {
    const mine = await apiJson("/api/v1/profiles/me/");
    if (mine.status === 404) {
      setProfile(null);
      return mine;
    }

    if (mine.ok) {
      setProfile(mine.data);
    }
    return mine;
  }

  const value = useMemo(
    () => ({
      user,
      profile,
      ready,
      login,
      register,
      logout,
      refreshProfile,
      loadSession,
    }),
    [user, profile, ready]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used inside AuthProvider");
  }
  return context;
}
