import { useState, useEffect } from "react";

function App() {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState("");
    const [ws, setWs] = useState(null);

    useEffect(() => {
        const socket = new WebSocket("ws://localhost:8000/ws");

        socket.onopen = () => {
            console.log("✅ WebSocket connected");
            setWs(socket);
        };

        socket.onmessage = (event) => {
            try {
                const data = JSON.parse(event.data);
                console.log("📩 Received Data:", data);

                if (data.error) {
                    setMessages((prev) => [...prev, { text: data.error, sender: "bot" }]);
                } else {
                    data.forEach((recipe) => {
                        setMessages((prev) => [...prev, { text: recipe.title, sender: "bot" }]);
                    });
                }
            } catch (error) {
                console.error("❌ JSON Parse Error:", error);
            }
        };

        socket.onclose = () => console.log("❌ WebSocket Disconnected");

        return () => {
            socket.close();
        };
    }, []);

    const sendMessage = () => {
        if (input && ws) {
            ws.send(input);
            setMessages((prev) => [...prev, { text: input, sender: "user" }]);
            setInput("");
        }
    };

    return (
        <div>
            <h1>Recipe Bot 🍽️</h1>
            <div>
                {messages.map((msg, index) => (
                    <p key={index}>
                        <strong>{msg.sender}:</strong> {msg.text}
                    </p>
                ))}
            </div>
            <input value={input} onChange={(e) => setInput(e.target.value)} placeholder="Enter ingredients..." />
            <button onClick={sendMessage}>Search Recipes</button>
        </div>
    );
}

export default App;
