import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { apiJson, formatError, mediaUrl, resultsOf } from "../api";

export default function Chats() {
  const navigate = useNavigate();
  const [chats, setChats] = useState([]);
  const [error, setError] = useState("");
  const [search, setSearch] = useState("");

  const visibleChats = chats.filter((chat) =>
    [chat.profile?.display_name, chat.profile?.bio]
      .filter(Boolean)
      .join(" ")
      .toLowerCase()
      .includes(search.trim().toLowerCase())
  );

  useEffect(() => {
    apiJson("/api/v1/chats/").then((result) => {
      if (!result.ok) {
        setError(formatError(result.data));
        return;
      }
      setChats(resultsOf(result.data));
    });
  }, []);

  function formatTime(isoString) {
    if (!isoString) return "";
    const date = new Date(isoString);
    const now = new Date();
    const diffMs = now - date;
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);
    const diffDays = Math.floor(diffMs / 86400000);

    if (diffMins < 1) return "Now";
    if (diffMins < 60) return `${diffMins}m`;
    if (diffHours < 24) return `${diffHours}h`;
    if (diffDays < 7) return `${diffDays}d`;
    return date.toLocaleDateString([], { month: "short", day: "numeric" });
  }

  function getLastMessagePreview(chat) {
    if (!chat.last_message) {
      return "No messages yet";
    }
    return chat.last_message.content.length > 60
      ? chat.last_message.content.substring(0, 60) + "..."
      : chat.last_message.content;
  }

  return (
    <section className="page">
      <header className="page-head">
        <div>
          <p className="eyebrow">Chats</p>
          <h1>Conversations from your matches</h1>
        </div>
      </header>

      <input
        className="search-input"
        value={search}
        onChange={(event) => setSearch(event.target.value)}
        placeholder="Search conversations"
        aria-label="Search conversations"
      />

      {error && <p className="error-text">{error}</p>}

      {chats.length === 0 ? (
        <div className="empty-card">
          <h2>No conversations yet</h2>
          <p>Match with someone first. A chat is created automatically.</p>
        </div>
      ) : visibleChats.length === 0 ? (
        <div className="empty-card">
          <h2>No matching conversations</h2>
          <p>Try a different name or keyword.</p>
        </div>
      ) : (
        <div className="chat-list">
          {visibleChats.map((chat) => (
            <Link
              key={chat.uuid}
              to={`/chats/${chat.uuid}`}
              className="chat-row-link"
            >
              <div className="chat-row">
                <div className="chat-avatar">
                  {chat.profile?.photo ? (
                    <img src={mediaUrl(chat.profile.photo)} alt="" />
                  ) : (
                    <span className="avatar-fallback">
                      {chat.profile?.display_name?.[0] || "?"}
                    </span>
                  )}
                </div>
                <div className="chat-content">
                  <div className="chat-header">
                    <h3>{chat.profile?.display_name}</h3>
                    <span className="chat-time">
                      {formatTime(chat.last_message_at)}
                    </span>
                  </div>
                  <p className="chat-preview">
                    {getLastMessagePreview(chat)}
                  </p>
                </div>
              </div>
            </Link>
          ))}
        </div>
      )}
    </section>
  );
}
