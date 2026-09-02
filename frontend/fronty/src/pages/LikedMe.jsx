import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { apiJson, formatError, mediaUrl, resultsOf } from "../api";

export default function LikedMe() {
  const navigate = useNavigate();
  const [profiles, setProfiles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  async function loadLikedMe() {
    setLoading(true);
    setError("");

    const result = await apiJson("/api/v1/interactions/liked-me/");

    if (!result.ok) {
      setError(formatError(result.data));
      setLoading(false);
      return;
    }

    setProfiles(resultsOf(result.data));
    setLoading(false);
  }

  useEffect(() => {
    loadLikedMe();
  }, []);

  function avatarSrc(profile) {
    const photos = profile?.photos || [];
    const photo =
      photos.find((item) => item.is_profile_picture) || photos[0];

    return photo ? mediaUrl(photo.image) : "";
  }

  if (loading) {
    return (
      <section className="page">
        <h1>Liked Me</h1>
        <p>Loading...</p>
      </section>
    );
  }

  return (
    <section className="page">
      <header>
        <h1>Liked Me</h1>
        <p className="muted">
          People who liked you, but you haven't liked back yet.
        </p>
      </header>

      {error && <p className="error-text">{error}</p>}

      {!error && profiles.length === 0 && (
        <div>
          <h3>No new likes</h3>
          <p className="muted">
            Nobody has liked you without a match yet.
          </p>
        </div>
      )}

      <div className="profile-grid">
        {profiles.map((profile) => {
          const src = avatarSrc(profile);

          return (
            <article className="profile-card" key={profile.uuid} onClick={() => profile?.uuid && navigate(`/profile/${profile.uuid}`)} style={{ cursor: profile?.uuid ? 'pointer' : 'default' }}>
              <div className="profile-card-photo">
                {src ? (
                  <img src={src} alt={profile.display_name} />
                ) : (
                  <div className="profile-placeholder">
                    {profile.display_name?.[0] || "?"}
                  </div>
                )}
              </div>

              <div className="profile-card-body">
                <h2>{profile.display_name}</h2>

                {profile.bio && (
                  <p className="muted">{profile.bio}</p>
                )}

                <div style={{ display: 'flex', gap: '8px' }}>
                  <button
                    type="button"
                    onClick={(e) => {
                      e.stopPropagation();
                      (async () => {
                        const result = await apiJson(
                          "/api/v1/interactions/",
                          {
                            method: "POST",
                            body: JSON.stringify({
                              profile_uuid: profile.uuid,
                              action: "LIKE",
                            }),
                          }
                        );

                        if (result.ok) {
                          setProfiles((current) =>
                            current.filter(
                              (item) => item.uuid !== profile.uuid
                            )
                          );
                        } else {
                          setError(formatError(result.data));
                        }
                      })();
                    }}
                  >
                    ❤️ Like Back
                  </button>
                  <button
                    type="button"
                    className="ghost"
                    onClick={(e) => {
                      e.stopPropagation();
                      (async () => {
                        const result = await apiJson(
                          "/api/v1/interactions/",
                          {
                            method: "POST",
                            body: JSON.stringify({
                              profile_uuid: profile.uuid,
                              action: "PASS",
                            }),
                          }
                        );

                        if (result.ok) {
                          setProfiles((current) =>
                            current.filter(
                              (item) => item.uuid !== profile.uuid
                            )
                          );
                        } else {
                          setError(formatError(result.data));
                        }
                      })();
                    }}
                  >
                    ✕ Pass
                  </button>
                </div>
              </div>
            </article>
          );
        })}
      </div>
    </section>
  );
}
