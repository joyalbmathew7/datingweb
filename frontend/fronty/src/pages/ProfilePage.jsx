import { useEffect, useState } from "react";
import { apiJson, formatError, mediaUrl, resultsOf } from "../api";
import { useAuth } from "../AuthContext";

const GENDERS = [
  ["MAN", "Man"],
  ["WOMAN", "Woman"],
  ["NON_BINARY", "Non-binary"],
  ["PREFER_NOT_TO_SAY", "Prefer not to say"],
];

const INTERESTED_IN = [
  ["MEN", "Men"],
  ["WOMEN", "Women"],
  ["EVERYONE", "Everyone"],
];

const RELATIONSHIP = [
  ["SINGLE", "Single"],
  ["IN_RELATIONSHIP", "In a relationship"],
];

export default function ProfilePage() {
  const { profile, refreshProfile, user } = useAuth();
  const [form, setForm] = useState(null);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [oldPassword, setOldPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [countries, setCountries] = useState([]);
  const [states, setStates] = useState([]);
  const [cities, setCities] = useState([]);
  const [countrySearch, setCountrySearch] = useState("");
  const [stateSearch, setStateSearch] = useState("");
  const [citySearch, setCitySearch] = useState("");
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);
  const [deletingAccount, setDeletingAccount] = useState(false);
  const [deleteError, setDeleteError] = useState("");

  useEffect(() => {
    if (!profile) return;
    setForm({
      display_name: profile.display_name || "",
      bio: profile.bio || "",
      date_of_birth: profile.date_of_birth || "",
      gender: profile.gender || "MAN",
      interested_in: profile.interested_in || "EVERYONE",
      relationship_status: profile.relationship_status || "SINGLE",
      country: profile.country,
      state: profile.state,
      city: profile.city,
    });
  }, [profile]);

  useEffect(() => {
    apiJson("/api/v1/locations/countries/").then((result) => {
      if (result.ok) setCountries(resultsOf(result.data));
    });
  }, []);

  useEffect(() => {
    if (!form?.country) return;
    apiJson(`/api/v1/locations/states/?country=${form.country}`).then((result) => {
      if (result.ok) setStates(resultsOf(result.data));
    });
  }, [form?.country]);

  useEffect(() => {
    if (!form?.state) return;
    apiJson(`/api/v1/locations/cities/?state=${form.state}`).then((result) => {
      if (result.ok) setCities(resultsOf(result.data));
    });
  }, [form?.state]);

  function update(field, value) {
    setForm((current) => ({ ...current, [field]: value }));
  }

  const filteredCountries = countries.filter((country) =>
    country.name.toLowerCase().includes(countrySearch.trim().toLowerCase())
  );
  const filteredStates = states.filter((state) =>
    state.name.toLowerCase().includes(stateSearch.trim().toLowerCase())
  );
  const filteredCities = cities.filter((city) =>
    city.name.toLowerCase().includes(citySearch.trim().toLowerCase())
  );

  async function saveProfile(event) {
    event.preventDefault();
    setError("");
    setMessage("");

    const result = await apiJson("/api/v1/profiles/me/update/", {
      method: "PATCH",
      body: JSON.stringify(form),
    });

    if (!result.ok) {
      setError(formatError(result.data));
      return;
    }

    await refreshProfile();
    setMessage("Profile updated.");
  }

  async function uploadPhoto(event) {
    const file = event.target.files?.[0];
    if (!file) return;

    const body = new FormData();
    body.append("image", file);

    const result = await apiJson("/api/v1/profiles/photos/", {
      method: "POST",
      body,
    });

    event.target.value = "";

    if (!result.ok) {
      setError(formatError(result.data));
      return;
    }

    await refreshProfile();
    setMessage("Photo uploaded.");
  }

  async function setPicture(photoUuid) {
    const result = await apiJson(
      `/api/v1/profiles/photos/${photoUuid}/profile-picture/`,
      { method: "PATCH" }
    );
    if (!result.ok) {
      setError(formatError(result.data));
      return;
    }
    await refreshProfile();
  }

  async function deletePhoto(photoUuid) {
    const result = await apiJson(`/api/v1/profiles/photos/${photoUuid}/`, {
      method: "DELETE",
    });
    if (!result.ok && result.status !== 204) {
      setError(formatError(result.data));
      return;
    }
    await refreshProfile();
  }

  async function changePassword(event) {
    event.preventDefault();
    setError("");
    setMessage("");

    const result = await apiJson("/api/v1/auth/change-password/", {
      method: "PUT",
      body: JSON.stringify({
        old_password: oldPassword,
        new_password: newPassword,
      }),
    });

    if (!result.ok) {
      setError(formatError(result.data));
      return;
    }

    setOldPassword("");
    setNewPassword("");
    setMessage(result.data.message || "Password changed.");
  }

  if (!form) return null;

  return (
    <section className="page profile-page">
      <header className="page-head">
        <div>
          <p className="eyebrow">Your profile</p>
          <h1>{form.display_name}</h1>
          <p className="muted">
            {user?.username} · {user?.email}
          </p>
        </div>
      </header>

      {error && <p className="error-text">{error}</p>}
      {message && <p className="ok-text">{message}</p>}

      <div className="photo-grid">
        {(profile.photos || []).map((photo) => (
          <figure key={photo.uuid} className="photo-tile">
            <img src={mediaUrl(photo.image)} alt="" />
            <figcaption>
              {photo.is_profile_picture ? "Profile photo" : "Gallery"}
              <span>
                <button type="button" onClick={() => setPicture(photo.uuid)}>
                  Set as face
                </button>
                <button type="button" onClick={() => deletePhoto(photo.uuid)}>
                  Remove
                </button>
              </span>
            </figcaption>
          </figure>
        ))}
        <label className="photo-upload">
          Add photo
          <input type="file" accept="image/*" onChange={uploadPhoto} hidden />
        </label>
      </div>

      <form className="profile-form" onSubmit={saveProfile}>
        <label>
          Display name
          <input
            value={form.display_name}
            onChange={(event) => update("display_name", event.target.value)}
          />
        </label>
        <label>
          Bio
          <textarea
            value={form.bio}
            onChange={(event) => update("bio", event.target.value)}
            rows={4}
            maxLength={500}
          />
        </label>
        <label>
          Date of birth
          <input
            type="date"
            value={form.date_of_birth}
            onChange={(event) => update("date_of_birth", event.target.value)}
          />
        </label>
        <div className="grid-2">
          <label>
            Gender
            <select
              value={form.gender}
              onChange={(event) => update("gender", event.target.value)}
            >
              {GENDERS.map(([value, label]) => (
                <option key={value} value={value}>
                  {label}
                </option>
              ))}
            </select>
          </label>
          <label>
            Interested in
            <select
              value={form.interested_in}
              onChange={(event) => update("interested_in", event.target.value)}
            >
              {INTERESTED_IN.map(([value, label]) => (
                <option key={value} value={value}>
                  {label}
                </option>
              ))}
            </select>
          </label>
        </div>
        <label>
          Relationship status
          <select
            value={form.relationship_status}
            onChange={(event) => update("relationship_status", event.target.value)}
          >
            {RELATIONSHIP.map(([value, label]) => (
              <option key={value} value={value}>
                {label}
              </option>
            ))}
          </select>
        </label>
        <div className="grid-3">
          <label>
            Country
            <input
              value={countrySearch}
              onChange={(event) => setCountrySearch(event.target.value)}
              placeholder="Search countries"
              aria-label="Search countries"
            />
            <select
              value={form.country || ""}
              onChange={(event) =>
                setForm((current) => ({ ...current, country: Number(event.target.value), state: "", city: "" }))
              }
              required
            >
              <option value="">Select</option>
              {filteredCountries.map((country) => <option key={country.id} value={country.id}>{country.name}</option>)}
            </select>
          </label>
          <label>
            State
            <input
              value={stateSearch}
              onChange={(event) => setStateSearch(event.target.value)}
              placeholder="Search states"
              aria-label="Search states"
              disabled={!form.country}
            />
            <select
              value={form.state || ""}
              onChange={(event) =>
                setForm((current) => ({ ...current, state: Number(event.target.value), city: "" }))
              }
              required
            >
              <option value="">Select</option>
              {filteredStates.map((state) => <option key={state.id} value={state.id}>{state.name}</option>)}
            </select>
          </label>
          <label>
            City
            <input
              value={citySearch}
              onChange={(event) => setCitySearch(event.target.value)}
              placeholder="Search cities"
              aria-label="Search cities"
              disabled={!form.state}
            />
            <select value={form.city || ""} onChange={(event) => update("city", Number(event.target.value))} required>
              <option value="">Select</option>
              {filteredCities.map((city) => <option key={city.id} value={city.id}>{city.name}</option>)}
            </select>
          </label>
        </div>
        <button type="submit">Save profile</button>
      </form>

      <form className="profile-form" onSubmit={changePassword}>
        <h3>Change password</h3>
        <label>
          Current password
          <input
            type="password"
            value={oldPassword}
            onChange={(event) => setOldPassword(event.target.value)}
            required
          />
        </label>
        <label>
          New password
          <input
            type="password"
            value={newPassword}
            onChange={(event) => setNewPassword(event.target.value)}
            minLength={8}
            required
          />
        </label>
        <button type="submit">Update password</button>
      </form>
      <div className="danger-zone">
  <h3>Danger Zone</h3>

  <button
    type="button"
    onClick={() => {
      setDeleteError("");
      setShowDeleteConfirm(true);
    }}
    className="delete-account-button"
  >
    Delete Account
  </button>
  {showDeleteConfirm && (
  <div className="delete-confirmation">
    <h3>Delete your account?</h3>

    <p>
      This action cannot be undone. Your account and its data will be deleted.
    </p>

    {deleteError && (
      <p className="error-text">
        {deleteError}
      </p>
    )}

    <button
      type="button"
      onClick={() => setShowDeleteConfirm(false)}
      disabled={deletingAccount}
    >
      Cancel
    </button>

    <button
      type="button"
      onClick={deleteAccount}
      disabled={deletingAccount}
    >
      {deletingAccount ? "Deleting..." : "Yes, Delete My Account"}
    </button>
  </div>
)}
</div>
    </section>
  );
  async function deleteAccount() {
      setDeletingAccount(true);
      setDeleteError("");

      const result = await apiJson("/api/v1/auth/account/", {
        method: "DELETE",
      });

      if (!result.ok) {
        setDeleteError(
          result.data?.detail || "Failed to delete account."
        );
        setDeletingAccount(false);
        return;
      }

      // Account deleted successfully
      localStorage.clear();

      window.location.href = "/login";
    }
  
}
