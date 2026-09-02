import { useEffect, useRef, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import { apiJson, formatError, getUsableAccessToken, resultsOf } from "../api";
import { useAuth } from "../AuthContext";

function wsUrl(conversationUuid, token) {
  const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
  const configuredOrigin = import.meta.env.VITE_WS_ORIGIN;
  const origin = configuredOrigin
    ? configuredOrigin.replace(/^https?:/, protocol)
    : window.location.port === "5173"
      ? `${protocol}//${window.location.hostname}:8000`
      : `${protocol}//${window.location.host}`;
  return `${origin}/ws/chats/${conversationUuid}/?token=${encodeURIComponent(token)}`;
}

export default function ChatThread() {
  const navigate = useNavigate();
  const { uuid } = useParams();
  const { profile } = useAuth();
  const [conversation, setConversation] = useState(null);
  const [messages, setMessages] = useState([]);
  const [draft, setDraft] = useState("");
  const [error, setError] = useState("");
  const [blockedNote, setBlockedNote] = useState("");
  const [canSend, setCanSend] = useState(true);
  const [messageSearch, setMessageSearch] = useState("");
  const [live, setLive] = useState(false);
  const socketRef = useRef(null);
  const bottomRef = useRef(null);
  // const seenRef = useRef(new Set());
  const reconnectTimerRef = useRef(null);

function addMessages(incoming) {
  console.log("[chat] addMessages called", incoming);

  setMessages((current) => {
    const existingUuids = new Set(
      current.map((message) => message.uuid)
    );

    const newMessages = incoming.filter((message) => {
      if (!message?.uuid) {
        console.log("[chat] message skipped", {
          message,
          reason: "missing uuid",
        });
        return false;
      }

      if (existingUuids.has(message.uuid)) {
        console.log("[chat] message skipped", {
          message,
          reason: "duplicate uuid",
        });
        return false;
      }

      existingUuids.add(message.uuid);
      return true;
    });

    const next = [...current, ...newMessages];

    next.sort(
      (left, right) =>
        new Date(left.created_at) - new Date(right.created_at)
    );

    console.log("[chat] messages state will contain", next);

    return next;
  });
}

  async function loadConversation() {
    console.log("[chat] loading conversation and message history", uuid);
    const chats = await apiJson("/api/v1/chats/");
    if (chats.ok) {
      const found = resultsOf(chats.data).find((item) => item.uuid === uuid);
      setConversation(found || null);
    }

    const result = await apiJson(`/api/v1/chats/${uuid}/messages/`);
    if (!result.ok) {
      console.log("[chat] message history request failed", result);
      setError(formatError(result.data));
      return;
    }
    console.log("[chat] message history response", result.data);
    // seenRef.current = new Set();
    addMessages(resultsOf(result.data));
  }

  useEffect(() => {
    loadConversation();
  }, [uuid]);

  useEffect(() => {
    let disposed = false;
    let attempts = 0;

    async function connect() {
      const token = await getUsableAccessToken();
      if (!token || disposed) {
        if (!disposed) setError("Your session has expired. Please log in again.");
        return;
      }
      const socket = new WebSocket(wsUrl(uuid, token));
      socketRef.current = socket;
      console.log("[chat] WebSocket created", socket.url.replace(/token=[^&]+/, "token=<redacted>"));

      socket.onopen = () => {
        attempts = 0;
        setLive(true);
        console.log("[chat] WebSocket opened");
      };
      socket.onclose = () => {
        setLive(false);
        console.log("[chat] WebSocket closed", {
          readyState: socket.readyState,
          attempts,
        });
        if (!disposed && attempts < 4) {
          const delay = 800 * 2 ** attempts;
          attempts += 1;
          reconnectTimerRef.current = window.setTimeout(connect, delay);
        }
      };
      socket.onerror = (event) => {
        setLive(false);
        console.log("[chat] WebSocket error", event);
      };
      socket.onmessage = (event) => {
        console.log("[chat] WebSocket raw message", event.data);
        const payload = JSON.parse(event.data);
        console.log("[chat] WebSocket parsed message", payload);
        if (payload.type === "error") {
          setBlockedNote(payload.detail);
          setCanSend(false);
          return;
        }
        if (payload.type === "message") addMessages([payload]);
      };
    }

    connect();

    return () => {
      disposed = true;
      window.clearTimeout(reconnectTimerRef.current);
      socketRef.current?.close();
    };
  }, [uuid]);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  async function sendMessage(event) {
    event.preventDefault();
    const content = draft.trim();
    console.log("[chat] sendMessage", {
      content,
      canSend,
      socketReadyState: socketRef.current?.readyState,
      webSocketOpen: WebSocket.OPEN,
    });
    if (!content || !canSend) {
      console.log("[chat] sendMessage stopped before transport");
      return;
    }
    setDraft("");
    setBlockedNote("");

    const socket = socketRef.current;
    if (socket && socket.readyState === WebSocket.OPEN) {
      const payload = JSON.stringify({ content });
      console.log("[chat] sending WebSocket payload", payload);
      socket.send(payload);
      console.log("[chat] socket.send completed");
      return;
    }

    console.log("[chat] WebSocket not open; using HTTP fallback");
    const result = await apiJson(`/api/v1/chats/${uuid}/messages/`, {
      method: "POST",
      body: JSON.stringify({ content }),
    });

    if (!result.ok) {
      console.log("[chat] HTTP message send failed", result);
      setError(formatError(result.data));
      setDraft(content);
      return;
    }

    console.log("[chat] HTTP message send succeeded", result.data);
    addMessages([result.data]);
  }

  async function blockUser() {
    if (!conversation?.profile?.uuid) return;
    const result = await apiJson("/api/v1/interactions/block/", {
      method: "POST",
      body: JSON.stringify({ profile_uuid: conversation.profile.uuid }),
    });
    if (!result.ok) {
      setError(formatError(result.data));
      return;
    }
    setBlockedNote("You blocked this person. Old messages stay, new ones cannot be sent.");
    setCanSend(false);
  }

  async function unblockUser() {
    if (!conversation?.profile?.uuid) return;
    const result = await apiJson("/api/v1/interactions/unblock/", {
      method: "POST",
      body: JSON.stringify({ profile_uuid: conversation.profile.uuid }),
    });
    if (!result.ok) {
      setError(formatError(result.data));
      return;
    }
    setBlockedNote("");
    setCanSend(true);
  }

  const otherName = conversation?.profile?.display_name || "Chat";
  const visibleMessages = messages.filter((message) =>
    [message.sender?.display_name, message.content]
      .filter(Boolean)
      .join(" ")
      .toLowerCase()
      .includes(messageSearch.trim().toLowerCase())
  );

  useEffect(() => {
    console.log("[chat] render state", {
      messages,
      visibleMessages,
      messageSearch,
    });
  }, [messages, visibleMessages, messageSearch]);

  return (
    <section className="page chat-thread">
      <header className="thread-head">
        <div>
          <Link to="/chats" className="back-link">
            ← Conversations
          </Link>
          <h1 onClick={() => conversation?.profile?.uuid && navigate(`/profile/${conversation.profile.uuid}`)} style={{ cursor: conversation?.profile?.uuid ? 'pointer' : 'default' }}>{otherName}</h1>
        </div>
        <div className="thread-actions">
          <button type="button" className="ghost" onClick={blockUser}>
            Block
          </button>
          <button type="button" className="ghost" onClick={unblockUser}>
            Unblock
          </button>
        </div>
      </header>

      {error && <p className="error-text">{error}</p>}
      {blockedNote && <p className="warn-text">{blockedNote}</p>}

      <input
        className="search-input message-search"
        value={messageSearch}
        onChange={(event) => setMessageSearch(event.target.value)}
        placeholder="Search messages"
        aria-label="Search messages"
      />

      <div className="bubble-list">
        {visibleMessages.map((message) => {
          const mine = message.sender?.uuid === profile?.uuid;
          const timestamp = new Date(message.created_at).toLocaleTimeString([], {
            hour: "numeric",
            minute: "2-digit",
          });
          return (
            <div
              key={message.uuid}
              className={mine ? "bubble mine" : "bubble theirs"}
            >
              <p>{message.content}</p>
              <small>{timestamp}</small>
            </div>
          );
        })}
        <div ref={bottomRef} />
      </div>

      <form className="composer" onSubmit={sendMessage}>
        <input
          value={draft}
          onChange={(event) => setDraft(event.target.value)}
          placeholder={`Message ${otherName}`}
          disabled={!canSend}
        />
        <button type="submit" disabled={!canSend}>Send</button>
      </form>
    </section>
  );
}
