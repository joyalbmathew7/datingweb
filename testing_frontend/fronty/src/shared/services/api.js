const API_BASE_URL = "http://127.0.0.1:8000/api/v1/auth";

export async function apiRequest(endpoint, options = {}) {
    const accessToken = localStorage.getItem("access");

    const response = await fetch(
        `${API_BASE_URL}${endpoint}`,
        {
            ...options,

            headers: {
                "Content-Type": "application/json",
                ...(accessToken && {
                    Authorization: `Bearer ${accessToken}`,
                }),
                ...options.headers,
            },
        }
    );

    const data = await response.json();

    if (!response.ok) {
        throw data;
    }

    return data;
}
