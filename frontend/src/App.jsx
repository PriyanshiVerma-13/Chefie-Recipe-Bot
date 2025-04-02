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
            console.log("📩 Received:", event.data);
            const message = { text: event.data, sender: "bot" };
            setMessages((prev) => [...prev, message]);
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
        <div style={styles.container}>
            <h1>🍽️ RecipeBot</h1>
            <div style={styles.chatBox}>
                {messages.map((msg, index) => (
                    <div key={index} style={msg.sender === "user" ? styles.userMessage : styles.botMessage}>
                        <strong>{msg.sender}:</strong> {msg.text}
                    </div>
                ))}
            </div>
            <div style={styles.inputContainer}>
                <input 
                    value={input} 
                    onChange={(e) => setInput(e.target.value)} 
                    placeholder="Enter ingredients or ask a question..."
                    style={styles.input}
                />
                <button onClick={sendMessage} style={styles.button}>Send</button>
            </div>
        </div>
    );
}

// 💡 Inline CSS for simple styling
const styles = {
    container: { textAlign: "center", fontFamily: "Arial, sans-serif", padding: 20 },
    chatBox: { maxHeight: "300px", overflowY: "auto", border: "1px solid #ddd", padding: 10, marginBottom: 10 },
    userMessage: { textAlign: "right", color: "blue", marginBottom: 5 },
    botMessage: { textAlign: "left", color: "green", marginBottom: 5 },
    inputContainer: { display: "flex", justifyContent: "center", gap: 10 },
    input: { padding: 10, width: "60%", borderRadius: 5, border: "1px solid #ddd" },
    button: { padding: "10px 15px", background: "blue", color: "white", border: "none", cursor: "pointer" }
};

export default App;
