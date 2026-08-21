import { useEffect, useRef, useState } from "react";

function ChatWindow({ conversationUuid, accessToken }) {
    const [messages, setMessages] = useState([]);
    const [content, setContent] = useState("");

    const socketRef = useRef(null);

    useEffect(() => {
        if (!conversationUuid || !accessToken) {
            return;
        }

        console.log("Connecting to WebSocket...");

        const socket = new WebSocket(
            `ws://127.0.0.1:8000/ws/chats/${conversationUuid}/?token=${accessToken}`
        );

        socketRef.current = socket;

        socket.onopen = () => {
            console.log("WebSocket connected!");
        };

        socket.onmessage = (event) => {
            console.log("Raw message received:", event.data);

            const data = JSON.parse(event.data);

            console.log("Parsed message:", data);

            if (data.type === "message") {
                setMessages((previous) => [
                    ...previous,
                    data,
                ]);
            }
        };

        socket.onerror = (error) => {
            console.error("WebSocket error:", error);
        };

        socket.onclose = (event) => {
            console.log(
                "WebSocket disconnected!",
                event.code,
                event.reason
            );
        };

        return () => {
            socket.close();
        };
    }, [conversationUuid, accessToken]);

    const sendMessage = () => {
        if (!content.trim()) {
            return;
        }

        if (
            !socketRef.current ||
            socketRef.current.readyState !== WebSocket.OPEN
        ) {
            console.log("WebSocket is not connected!");
            return;
        }

        console.log("Sending:", content);

        socketRef.current.send(
            JSON.stringify({
                content: content,
            })
        );

        setContent("");
    };

    return (
        <div>
            <h2>Chat</h2>

            <div>
                {messages.map((message) => (
                    <div key={message.uuid}>
                        <strong>
                            {message.sender.display_name}
                        </strong>

                        <p>{message.content}</p>
                    </div>
                ))}
            </div>

            <input
                type="text"
                value={content}
                onChange={(event) => {
                    setContent(event.target.value);
                }}
                placeholder="Type a message..."
            />

            <button onClick={sendMessage}>
                Send
            </button>
        </div>
    );
}

export default ChatWindow;