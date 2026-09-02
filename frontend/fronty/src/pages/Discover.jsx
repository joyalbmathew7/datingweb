import { useEffect, useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";
import { ageFromDob, apiJson, formatError, mediaUrl, resultsOf } from "../api";

function profilePhoto(person) {
  const photos = person?.photos || [];
  const pictured =
    photos.find((photo) => photo.is_profile_picture) || photos[0];
  return pictured ? mediaUrl(pictured.image) : "";
}

export default function Discover() {
  const navigate = useNavigate();
  const [people, setPeople] = useState([]);
  const [index, setIndex] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [matchToast, setMatchToast] = useState(null);
  const [search, setSearch] = useState("");
  const [filters, setFilters] = useState({
    gender: "",
    interested_in: "",
    relationship_status: "",
  });

  const discoverablePeople = people.filter((person) => {
    const text = [person.display_name, person.bio, person.city_name, person.state_name]
      .filter(Boolean)
      .join(" ")
      .toLowerCase();
    return text.includes(search.trim().toLowerCase());
  });
  const current = discoverablePeople[index] || null;

  const query = useMemo(() => {
    const params = new URLSearchParams();
    if (search.trim()) params.set("search", search.trim());
    Object.entries(filters).forEach(([key, value]) => {
      if (value) params.set(key, value);
    });
    const text = params.toString();
    return text ? `?${text}` : "";
  }, [filters, search]);

  async function loadPeople() {
    setLoading(true);
    setError("");
    const result = await apiJson(`/api/v1/discovery/${query}`);
    setLoading(false);

    if (!result.ok) {
      setError(formatError(result.data));
      setPeople([]);
      return;
    }

    setPeople(resultsOf(result.data));
    setIndex(0);
  }

  useEffect(() => {
    loadPeople();
  }, [query]);

  async function interact(action) {
    if (!current) return;

    const result = await apiJson("/api/v1/interactions/", {
      method: "POST",
      body: JSON.stringify({
        profile_uuid: current.uuid,
        action,
      }),
    });

    if (!result.ok) {
      setError(formatError(result.data));
      return;
    }

    if (result.data.match) {
      setMatchToast(result.data.match);
      setTimeout(() => setMatchToast(null), 2800);
    }

    setIndex((value) => value + 1);
  }

  const remaining = discoverablePeople.slice(index);
  const photo = profilePhoto(current);
  const age = ageFromDob(current?.date_of_birth);

  return (
    <section className="page discover-page">
      <header className="page-head">
        <div>
          <p className="eyebrow">Discover</p>
          <h1>People near you first</h1>
        </div>
      </header>

      <div className="filter-row">
        <input
          className="search-input"
          value={search}
          onChange={(event) => {
            setSearch(event.target.value);
            setIndex(0);
          }}
          placeholder="Search by name, bio, or place"
          aria-label="Search profiles"
        />
        <select
          value={filters.gender}
          onChange={(event) =>
            setFilters((currentFilters) => ({
              ...currentFilters,
              gender: event.target.value,
            }))
          }
        >
          <option value="">Any gender</option>
          <option value="MAN">Man</option>
          <option value="WOMAN">Woman</option>
          <option value="NON_BINARY">Non-binary</option>
        </select>

        <select
          value={filters.interested_in}
          onChange={(event) =>
            setFilters((currentFilters) => ({
              ...currentFilters,
              interested_in: event.target.value,
            }))
          }
        >
          <option value="">Any interest</option>
          <option value="MEN">Interested in men</option>
          <option value="WOMEN">Interested in women</option>
          <option value="EVERYONE">Interested in everyone</option>
        </select>

        <select
          value={filters.relationship_status}
          onChange={(event) =>
            setFilters((currentFilters) => ({
              ...currentFilters,
              relationship_status: event.target.value,
            }))
          }
        >
          <option value="">Any status</option>
          <option value="SINGLE">Single</option>
          <option value="IN_RELATIONSHIP">In a relationship</option>
        </select>
      </div>

      {error && <p className="error-text">{error}</p>}

      {loading ? (
        <div className="empty-card">Looking around…</div>
      ) : remaining.length === 0 ? (
        <div className="empty-card">
          <h2>That’s everyone for now</h2>
          <p>Try another filter, or come back after more people join.</p>
        </div>
      ) : (
        <div className="card-stage">
          <article
                className="person-card"
                onClick={() => current?.uuid && navigate(`/profile/${current.uuid}`)}
                style={{ cursor: current?.uuid ? "pointer" : "default" }}
              >
            <div className="person-photo">
              {photo ? (
                <img src={photo} alt={current.display_name} />
              ) : (
                <div className="photo-fallback">{current.display_name[0]}</div>
              )}
              <div className="person-meta">
                <h2>
                  {current.display_name}
                  {age ? <span> {age}</span> : null}
                </h2>
                <p>
                  {[current.city_name, current.state_name]
                    .filter(Boolean)
                    .join(", ")}
                </p>
              </div>
            </div>
            <div className="person-body">
              <p>{current.bio || "No bio yet."}</p>
              <div className="chip-row">
                <span className="chip">{current.gender}</span>
                <span className="chip">{current.interested_in}</span>
                <span className="chip">{current.relationship_status}</span>
              </div>
            </div>
          </article>

          <div className="action-row">
            <button type="button" className="ghost" onClick={(e) => { e.stopPropagation(); interact("PASS"); }}>
              Pass
            </button>
            <button type="button" className="like" onClick={(e) => { e.stopPropagation(); interact("LIKE"); }}>
              Like
            </button>
          </div>
        </div>
      )}

      {matchToast && (
        <div className="match-toast">
          It’s a match with {matchToast.profile_one} & {matchToast.profile_two}
        </div>
      )}
    </section>
  );
}
