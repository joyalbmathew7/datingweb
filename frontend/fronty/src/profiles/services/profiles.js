import { apiJson } from "../../shared/services/api";

export async function createProfile(formData) {
    return apiJson("/api/v1/profiles/", {
        method: "POST",
        body: formData,
    });
}

export async function getMyProfile() {
    return apiJson("/api/v1/profiles/me/");
}

export async function updateProfile(data) {
    return apiJson("/api/v1/profiles/me/update/", {
        method: "PATCH",
        body: JSON.stringify(data),
    });
}

export async function uploadPhoto(formData) {
    return apiJson("/api/v1/profiles/photos/", {
        method: "POST",
        body: formData,
    });
}

export async function deletePhoto(uuid) {
    return apiJson(`/api/v1/profiles/photos/${uuid}/`, {
        method: "DELETE",
    });
}

export async function setProfilePicture(uuid) {
    return apiJson(
        `/api/v1/profiles/photos/${uuid}/profile-picture/`,
        {
            method: "PATCH",
        }
    );
}
