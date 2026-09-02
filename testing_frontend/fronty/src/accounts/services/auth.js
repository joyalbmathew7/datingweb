import { apiRequest } from "../../shared/services/api";

export function registerUser(userData) {
    return apiRequest("/register/", {
        method: "POST",
        body: JSON.stringify(userData),
    });
}


export function verifyEmail(data) {
    return apiRequest("/verify-email/", {
        method: "POST",
        body: JSON.stringify(data),
    });
}

export function loginUser(data) {
    return apiRequest("/login/", {
        method: "POST",
        body: JSON.stringify(data),
    });
}

export function getCurrentUser() {
    const accessToken = localStorage.getItem("access");

    return apiRequest("/me/", {
        method: "GET",
        headers: {
            Authorization: `Bearer ${accessToken}`,
        },
    });
}

export function forgotPassword(data) {
    return apiRequest("/forgot-password/", {
        method: "POST",
        body: JSON.stringify(data),
    });
}


export function verifyPasswordOTP(data) {
    return apiRequest("/forgot-password/verify/", {
        method: "POST",
        body: JSON.stringify(data),
    });
}

export function resetPassword(data) {
    return apiRequest("/forgot-password/reset/", {
        method: "POST",
        body: JSON.stringify(data),
    });
}


export function logoutUser() {
    const refreshToken = localStorage.getItem("refresh");

    return apiRequest("/logout/", {
        method: "POST",
        body: JSON.stringify({
            refresh: refreshToken,
        }),
    });
}
