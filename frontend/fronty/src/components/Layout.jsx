import { NavLink, Outlet, useNavigate } from "react-router-dom";
import { useAuth } from "../AuthContext";
import { mediaUrl } from "../api";

function avatarSrc(profile) {
  const photos = profile?.photos || [];
  const pictured =
    photos.find((photo) => photo.is_profile_picture) || photos[0];
  return pictured ? mediaUrl(pictured.image) : "";
}

export default function Layout() {
  const { profile, logout } = useAuth();
  const navigate = useNavigate();
  const src = avatarSrc(profile);

  async function handleLogout() {
    await logout();
    navigate("/login");
  }

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <span className="brand-mark">K</span>
          <div>
            <strong>Kindred</strong>
            <p>Find someone close.</p>
          </div>
        </div>

        <nav className="side-nav">
          <NavLink to="/discover">Discover</NavLink>
          <NavLink to="/matches">Matches</NavLink>
          <NavLink to="/chats">Chats</NavLink>
            <NavLink to="/notifications">🔔 Notifications</NavLink>
            <NavLink to="/liked-me">Liked Me</NavLink>
          <NavLink to="/profile">Profile</NavLink>
        </nav>

        <div className="side-user">
          <div className="mini-avatar">
            {src ? <img src={src} alt="" /> : (profile?.display_name?.[0] || "?")}
          </div>
          <div>
            <strong>{profile?.display_name}</strong>
            <button type="button" className="link-btn" onClick={handleLogout}>
              Log out
            </button>
          </div>
        </div>
      </aside>

      <main className="main-pane">
        <Outlet />
      </main>
    </div>
  );
}
