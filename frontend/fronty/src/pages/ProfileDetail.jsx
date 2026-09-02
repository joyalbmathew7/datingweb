import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { ageFromDob, apiJson, formatError, mediaUrl } from "../api";
import PhotoViewer from "../components/PhotoViewer";

export default function ProfileDetail() {
  const { uuid } = useParams();
  const navigate = useNavigate();

  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [viewerIndex, setViewerIndex] = useState(null);

  useEffect(() => {
    async function loadProfile() {
      const result = await apiJson(`/api/v1/profiles/${uuid}/`);

      setLoading(false);

      if (!result.ok) {
        setError(formatError(result.data));
        return;
      }

      setProfile(result.data);
    }

    loadProfile();
  }, [uuid]);

  if (loading) {
    return <div className="empty-card">Loading profile...</div>;
  }

  if (error) {
    return (
      <section className="page">
        <header className="thread-head" style={{ paddingBottom: '16px', marginBottom: '16px' }}>
          <div>
            <button type="button" className="back-link" onClick={() => navigate(-1)}>
              ← Back
            </button>
          </div>
        </header>

        <p className="error-text">{error}</p>
      </section>
    );
  }

  if (!profile) {
    return <div className="empty-card">Profile not found.</div>;
  }

  const age = ageFromDob(profile.date_of_birth);

  return (
    <section className="page">
      <header className="thread-head" style={{ marginBottom: '24px' }}>
        <div>
          <button type="button" className="back-link" onClick={() => navigate(-1)}>
            ← Back
          </button>
          <h1 style={{ marginTop: '12px', marginBottom: '4px' }}>
            {profile.display_name}
            {age ? ` ${age}` : ""}
          </h1>
        </div>
      </header>

      <div className="profile-detail">
        <div className="profile-detail-head">
          <p>{profile.bio || "No bio yet."}</p>

          <div className="chip-row">
            <span className="chip">{profile.gender}</span>
            <span className="chip">{profile.interested_in}</span>
            <span className="chip">
              {profile.relationship_status}
            </span>
          </div>

          <p>
            {[
              profile.city?.name,
              profile.state?.name,
              profile.country?.name,
            ]
              .filter(Boolean)
              .join(", ")}
          </p>
        </div>

        {profile.photos && profile.photos.length > 0 && (
          <div className="profile-photos">
            {profile.photos.map((photo, idx) => (
              <div
                key={photo.uuid}
                className="profile-photo-tile"
                onClick={() => setViewerIndex(idx)}
                role="button"
                tabIndex={0}
                onKeyDown={(e) => {
                  if (e.key === "Enter" || e.key === " ") {
                    e.preventDefault();
                    setViewerIndex(idx);
                  }
                }}
                aria-label={`View photo ${idx + 1} of ${profile.photos.length}`}
              >
                <img
                  src={mediaUrl(photo.image)}
                  alt={`${profile.display_name} photo ${idx + 1}`}
                />
              </div>
            ))}
          </div>
        )}
      </div>

      {viewerIndex !== null && profile.photos && (
        <PhotoViewer
          photos={profile.photos}
          initialIndex={viewerIndex}
          onClose={() => setViewerIndex(null)}
        />
      )}
    </section>
  );
}

