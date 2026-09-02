import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { apiJson, formatError, mediaUrl } from "../api";

export default function Notifications() {
  const navigate = useNavigate();
  const [notifications, setNotifications] = useState([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  async function loadNotifications() {
    setLoading(true);
    setError("");

    const result = await apiJson("/api/v1/notifications/");

    if (!result.ok) {
      setError(formatError(result.data));
      setLoading(false);
      return;
    }

    setNotifications(
      Array.isArray(result.data)
        ? result.data
        : result.data.results || []
    );

    setLoading(false);
  }

  useEffect(() => {
    loadNotifications();
  }, []);

  if (loading) {
    return (
      <section className="page">
        <h1>Notifications</h1>
        <p>Loading...</p>
      </section>
    );
  }

  return (
    <section className="page">
      <h1>Notifications</h1>

      {error && <p className="error-text">{error}</p>}

      {notifications.length === 0 ? (
        <p className="muted">No notifications yet.</p>
      ) : (
        <div>
          {notifications.map((notification) => {
            const photo = notification.actor?.photo;

            return (
              <div key={notification.uuid} style={{ display: 'flex', gap: '12px', alignItems: 'center', padding: '12px 0', borderBottom: '1px solid #e0e0e0' }}>
                <div onClick={() => notification?.actor?.uuid && navigate(`/profile/${notification.actor.uuid}`)} style={{ cursor: notification?.actor?.uuid ? 'pointer' : 'default', flexShrink: 0 }}>
                  {photo ? (
                    <img
                      src={mediaUrl(photo)}
                      alt=""
                      width="50"
                      height="50"
                      style={{ borderRadius: '50%' }}
                    />
                  ) : (
                    <div style={{ width: '50px', height: '50px', borderRadius: '50%', backgroundColor: '#e0e0e0', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                      {notification.actor?.display_name?.[0] || '?'}
                    </div>
                  )}
                </div>

                <div style={{ flex: 1 }}>
                  <strong
                    onClick={() => notification?.actor?.uuid && navigate(`/profile/${notification.actor.uuid}`)}
                    style={{ cursor: notification?.actor?.uuid ? 'pointer' : 'default' }}
                  >
                    {notification.actor?.display_name}
                  </strong>

                  <p>
                    {notification.type === "LIKE" &&
                      " liked you ❤️"}

                    {notification.type === "MATCH" &&
                      " matched with you 💕"}

                    {notification.type === "MESSAGE" &&
                      " sent you a message 💬"}
                  </p>

                  {!notification.is_read && (
                    <strong> New</strong>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      )}
    </section>
  );
}