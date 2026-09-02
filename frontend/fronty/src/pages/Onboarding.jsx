import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { apiJson, formatError } from "../api";
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

export default function Onboarding() {
  const { profile, refreshProfile } = useAuth();
  const navigate = useNavigate();
  const [countries, setCountries] = useState([]);
  const [states, setStates] = useState([]);
  const [cities, setCities] = useState([]);
  const [error, setError] = useState("");
  const [photo, setPhoto] = useState(null);
  const [busy, setBusy] = useState(false);
  const [form, setForm] = useState({
    display_name: "",
    bio: "",
    date_of_birth: "",
    gender: "MAN",
    interested_in: "EVERYONE",
    relationship_status: "SINGLE",
    country: "",
    state: "",
    city: "",
  });

  useEffect(() => {
    if (profile) {
      navigate("/discover", { replace: true });
    }
  }, [profile, navigate]);

  useEffect(() => {
    apiJson("/api/v1/locations/countries/").then((result) => {
      if (result.ok) setCountries(Array.isArray(result.data) ? result.data : []);
    });
  }, []);

  useEffect(() => {
    if (!form.country) {
      setStates([]);
      setCities([]);
      return;
    }

    apiJson(`/api/v1/locations/states/?country=${form.country}`).then((result) => {
      if (result.ok) setStates(Array.isArray(result.data) ? result.data : []);
    });
  }, [form.country]);

  useEffect(() => {
    if (!form.state) {
      setCities([]);
      return;
    }

    apiJson(`/api/v1/locations/cities/?state=${form.state}`).then((result) => {
      if (result.ok) setCities(Array.isArray(result.data) ? result.data : []);
    });
  }, [form.state]);

  function update(field, value) {
    setForm((current) => ({ ...current, [field]: value }));
  }

  async function handleSubmit(event) {
    event.preventDefault();
    setBusy(true);
    setError("");

    if (!photo) {
      setBusy(false);
      setError("Choose a profile photo to continue.");
      return;
    }

    const body = new FormData();
    Object.entries(form).forEach(([key, value]) => body.append(key, value));
    body.append("image", photo);

    const result = await apiJson("/api/v1/profiles/", {
      method: "POST",
      body,
    });

    setBusy(false);

    if (!result.ok) {
      setError(formatError(result.data));
      return;
    }

    await refreshProfile();
    navigate("/discover");
  }

  return (
    <div className="onboard-page">
      <form className="onboard-card" onSubmit={handleSubmit}>
        <p className="eyebrow">Almost there</p>
        <h1>Tell people who you are</h1>
        <p className="muted">You need a profile before you can discover anyone.</p>

        <label>
          Profile photo
          <input
            type="file"
            accept="image/*"
            onChange={(event) => setPhoto(event.target.files?.[0] || null)}
            required
          />
        </label>

        <label>
          Display name
          <input
            value={form.display_name}
            onChange={(event) => update("display_name", event.target.value)}
            required
          />
        </label>

        <label>
          Bio
          <textarea
            value={form.bio}
            onChange={(event) => update("bio", event.target.value)}
            maxLength={500}
            rows={4}
          />
        </label>

        <label>
          Date of birth
          <input
            type="date"
            value={form.date_of_birth}
            onChange={(event) => update("date_of_birth", event.target.value)}
            required
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
            <select
              value={form.country}
              onChange={(event) =>
                setForm((current) => ({
                  ...current,
                  country: event.target.value,
                  state: "",
                  city: "",
                }))
              }
              required
            >
              <option value="">Select</option>
              {countries.map((country) => (
                <option key={country.id} value={country.id}>
                  {country.name}
                </option>
              ))}
            </select>
          </label>

          <label>
            State
            <select
              value={form.state}
              onChange={(event) =>
                setForm((current) => ({
                  ...current,
                  state: event.target.value,
                  city: "",
                }))
              }
              required
            >
              <option value="">Select</option>
              {states.map((state) => (
                <option key={state.id} value={state.id}>
                  {state.name}
                </option>
              ))}
            </select>
          </label>

          <label>
            City
            <select
              value={form.city}
              onChange={(event) => update("city", event.target.value)}
              required
            >
              <option value="">Select</option>
              {cities.map((city) => (
                <option key={city.id} value={city.id}>
                  {city.name}
                </option>
              ))}
            </select>
          </label>
        </div>

        {countries.length === 0 && (
          <p className="muted">
            No locations yet. From the backend folder run{" "}
            <code>python manage.py seed_locations</code>.
          </p>
        )}

        {error && <p className="error-text">{error}</p>}

        <button type="submit" disabled={busy}>
          {busy ? "Saving…" : "Create profile"}
        </button>
      </form>
    </div>
  );
}
