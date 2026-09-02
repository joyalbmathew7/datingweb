import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { apiJson, formatError, mediaUrl, resultsOf } from "../api";

export default function Matches() {
  const navigate = useNavigate();
  const [matches, setMatches] = useState([]);
  const [chats, setChats] = useState([]);
  const [error, setError] = useState("");
  const [search, setSearch] = useState("");

  useEffect(() => {
    Promise.all([
      apiJson("/api/v1/matches/"),
      apiJson("/api/v1/chats/"),
    ]).then(([matchResult, chatResult]) => {
      if (!matchResult.ok) {
        setError(formatError(matchResult.data));
        return;
      }
      setMatches(resultsOf(matchResult.data));
      if (chatResult.ok) {
        setChats(resultsOf(chatResult.data));
      }
    });
  }, []);

  function conversationFor(profileUuid) {
    return chats.find((chat) => chat.profile?.uuid === profileUuid);
  }

  const visibleMatches = matches.filter((match) => {
    const person = match.profile || {};
    return [person.display_name, person.bio, person.gender, person.relationship_status]
      .filter(Boolean)
      .join(" ")
      .toLowerCase()
      .includes(search.trim().toLowerCase());
  });

  return (
    <section className="page">
      <header className="page-head">
        <div>
          <p className="eyebrow">Matches</p>
          <h1>People who liked you back</h1>
        </div>
      </header>

      <input
        className="search-input"
        value={search}
        onChange={(event) => setSearch(event.target.value)}
        placeholder="Search matches"
        aria-label="Search matches"
      />

      {error && <p className="error-text">{error}</p>}

      {matches.length === 0 ? (
        <div className="empty-card">
          <h2>No matches yet</h2>
          <p>Like someone on Discover. If they like you too, they show up here.</p>
        </div>
      ) : visibleMatches.length === 0 ? (
        <div className="empty-card">
          <h2>No matching people</h2>
          <p>Try a different name or keyword.</p>
        </div>
      ) : (
        <div className="match-grid">
          {visibleMatches.map((match) => {
            const person = match.profile || {};
            const chat = conversationFor(person.uuid);
            return (
              <article key={match.uuid} className="match-card" onClick={() => person?.uuid && navigate(`/profile/${person.uuid}`)} style={{ cursor: person?.uuid ? 'pointer' : 'default' }}>
                <div className="match-photo">
                  {person.photo ? (
                    <img src={mediaUrl(person.photo)} alt="" />
                  ) : (
                    <span>{person.display_name?.[0] || "?"}</span>
                  )}
                </div>
                <div>
                  <h3>{person.display_name}</h3>
                  <p className="muted">{person.bio || "No bio yet."}</p>
                  {chat ? (
                    <Link className="text-link" to={`/chats/${chat.uuid}`}>
                      Open chat
                    </Link>
                  ) : (
                    <p className="muted">Chat will appear after the match is ready.</p>
                  )}
                </div>
              </article>
            );
          })}
        </div>
      )}
    </section>
  );
}
