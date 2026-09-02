const ACCESS_KEY = "kindred_access";
const REFRESH_KEY = "kindred_refresh";
let refreshPromise = null;

export function getAccessToken() {
  return localStorage.getItem(ACCESS_KEY);
}

export function getRefreshToken() {
  return localStorage.getItem(REFRESH_KEY);
}

export function setTokens(access, refresh) {
  if (access) localStorage.setItem(ACCESS_KEY, access);
  if (refresh) localStorage.setItem(REFRESH_KEY, refresh);
}

export function clearTokens() {
  localStorage.removeItem(ACCESS_KEY);
  localStorage.removeItem(REFRESH_KEY);
}

async function refreshAccessToken() {
  if (refreshPromise) return refreshPromise;

  refreshPromise = (async () => {
  const refresh = getRefreshToken();
  if (!refresh) return false;

  const response = await fetch("/api/v1/auth/refresh/", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ refresh }),
  });

  if (!response.ok) {
    clearTokens();
    return false;
  }

  const data = await response.json();
  setTokens(data.access, data.refresh || refresh);
  return true;
  })();

  try {
    return await refreshPromise;
  } finally {
    refreshPromise = null;
  }
}

function tokenExpiresSoon(token) {
  try {
    const payload = JSON.parse(atob(token.split(".")[1]));
    return !payload.exp || payload.exp * 1000 < Date.now() + 30_000;
  } catch {
    return true;
  }
}

export async function getUsableAccessToken() {
  const token = getAccessToken();
  if (token && !tokenExpiresSoon(token)) return token;
  return (await refreshAccessToken()) ? getAccessToken() : null;
}

export async function api(path, options = {}) {
  const headers = { ...(options.headers || {}) };
  const token = getAccessToken();

  if (token) {
    headers.Authorization = `Bearer ${token}`;
  }

  const isFormData = options.body instanceof FormData;
  if (options.body && !isFormData && !headers["Content-Type"]) {
    headers["Content-Type"] = "application/json";
  }

  let response = await fetch(path, { ...options, headers });

  if (response.status === 401 && getRefreshToken()) {
    const refreshed = await refreshAccessToken();
    if (refreshed) {
      headers.Authorization = `Bearer ${getAccessToken()}`;
      response = await fetch(path, { ...options, headers });
    }
  }

  return response;
}

export async function apiJson(path, options = {}) {
  const response = await api(path, options);
  let data = null;

  const text = await response.text();
  if (text) {
    try {
      data = JSON.parse(text);
    } catch {
      data = { detail: text };
    }
  }

  return { ok: response.ok, status: response.status, data };
}

export function formatError(data) {
  if (!data) return "Something went wrong.";
  if (typeof data === "string") return data;
  if (data.detail) {
    if (Array.isArray(data.detail)) return data.detail.join(" ");
    if (typeof data.detail === "object") return JSON.stringify(data.detail);
    return String(data.detail);
  }

  const parts = [];
  for (const [key, value] of Object.entries(data)) {
    if (Array.isArray(value)) {
      parts.push(`${key}: ${value.join(" ")}`);
    } else if (typeof value === "string") {
      parts.push(`${key}: ${value}`);
    }
  }

  return parts.join(" ") || "Something went wrong.";
}

export function mediaUrl(path) {
  if (!path) return "";
  if (path.startsWith("http://") || path.startsWith("https://")) {
    try {
      const url = new URL(path);
      return url.href;
    } catch {
      return path;
    }
    return path;
  }
  if (path.startsWith("/media/") && window.location.port === "5173") {
    return `http://${window.location.hostname}:8000${path}`;
  }
  return path;
}

export function ageFromDob(dob) {
  if (!dob) return null;
  const birth = new Date(dob);
  if (Number.isNaN(birth.getTime())) return null;
  const today = new Date();
  let age = today.getFullYear() - birth.getFullYear();
  const month = today.getMonth() - birth.getMonth();
  if (month < 0 || (month === 0 && today.getDate() < birth.getDate())) {
    age -= 1;
  }
  return age;
}

export function resultsOf(data) {
  if (!data) return [];
  if (Array.isArray(data)) return data;
  if (Array.isArray(data.results)) return data.results;
  return [];
}
