"use client";
import { useEffect, useState } from "react";

const sockURL = process.env.NEXT_PUBLIC_SOCKET_URL || "ws://localhost:654321";
// const sockURL = "wss://flowstone-production.up.railway.app/socket:654321";

const WebSocketClient: React.FC = () => {
  const [messages, setMessages] = useState<string[]>([]);
  const [input, setInput] = useState<string>("");
  const [socket, setSocket] = useState<WebSocket | null>(null);

  useEffect(() => {
    // Initialize WebSocket connection
    const ws = new WebSocket(sockURL); // WebSocket server address
    setSocket(ws);

    ws.onopen = () => {
      console.log("Connected to WebSocket server");
    };

    ws.onmessage = (event: MessageEvent) => {
      console.log(`Message from server: ${event.data}`);
      setMessages((prev) => [...prev, event.data]);
    };

    ws.onclose = () => {
      console.log("WebSocket connection closed");
    };

    ws.onerror = (error: Event) => {
      console.error("WebSocket error:", error);
    };

    return () => {
      ws.close();
    };
  }, []);

  const sendMessage = () => {
    if (socket && socket.readyState === WebSocket.OPEN) {
      socket.send(input); // Send message to server
      setInput("");
    } else {
      console.error("WebSocket is not open");
    }
  };

  return (
    <div>
      <h1>WebSocket Client</h1>
      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Type a message"
      />
      <button onClick={sendMessage}>Send</button>
      <div>
        <h2>Messages:</h2>
        {messages.map((msg, idx) => (
          <p key={idx}>{msg}</p>
        ))}
      </div>
    </div>
  );
};

export default WebSocketClient;
