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
        <div style={styles.fullScreenContainer}>
            <h1 className="heading" style={styles.heading}>Chefie is happy to see you!</h1>
            <div className="chat-box" style={styles.chatBox}>
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
        fullScreenContainer: {
        height: "100vh",
        width: "100vw",
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        alignItems: "center",
        fontFamily: "Arial, sans-serif",
        backgroundColor: "#f9f9f9",
        padding: 20,
        boxSizing: "border-box"
    },
    heading: {
        color: "black",
        fontSize: "2.5rem",
        marginBottom: "20px"
    },
    chatBox: {
        width: "80%",
        height: "50%",
        overflowY: "auto",
        border: "1px solid #ddd",
        padding: 10,
        marginBottom: 20,
        backgroundColor: "#fff",
        borderRadius: "8px"
    },
    userMessage: {
        textAlign: "right",
        color: "blue",
        marginBottom: 5
    },
    botMessage: {
        textAlign: "left",
        color: "green",
        marginBottom: 5
    },
    inputContainer: {
        display: "flex",
        width: "80%",
        gap: 10
    },
    input: {
        flex: 1,
        padding: 10,
        borderRadius: 5,
        border: "1px solid #ddd"
    },
    button: {
        padding: "10px 20px",
        backgroundColor: "blue",
        color: "white",
        border: "none",
        borderRadius: 5,
        cursor: "pointer"
    }
};

export default App;
