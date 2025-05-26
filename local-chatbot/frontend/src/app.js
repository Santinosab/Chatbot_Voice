import React, { useState, useRef } from "react";
import axios from "axios";

function App() {
  const [messages, setMessages] = useState([{ from: "bot", text: "¡Hola! Háblame o escríbeme." }]);
  const [input, setInput] = useState("");
  const recognitionRef = useRef(null);

  const sendMessage = async (msg) => {
    const userMessage = { from: "user", text: msg };
    setMessages((prev) => [...prev, userMessage]);

    try {
      const response = await axios.post("http://192.168.42.78:8000/chat", { message: msg });
      const botText = response.data.response;
      const botMessage = { from: "bot", text: botText };
      setMessages((prev) => [...prev, botMessage]);
      speak(botText); // ← habla la respuesta
    } catch (err) {
      setMessages((prev) => [...prev, { from: "bot", text: "Error de conexión." }]);
    }

    setInput("");
  };

  const speak = (text) => {
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = "es-ES"; // Cambia según el idioma
    speechSynthesis.speak(utterance);
  };

  const handleVoiceInput = () => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) return alert("Tu navegador no soporta reconocimiento de voz.");

    if (!recognitionRef.current) {
      recognitionRef.current = new SpeechRecognition();
      recognitionRef.current.lang = "es-ES";
      recognitionRef.current.continuous = false;
      recognitionRef.current.interimResults = false;

      recognitionRef.current.onresult = (e) => {
        const transcript = e.results[0][0].transcript;
        sendMessage(transcript);
      };

      recognitionRef.current.onerror = (e) => {
        console.error("Error de voz:", e);
      };
    }

    recognitionRef.current.start();
  };

  return (
    <div style={{ padding: 20, fontFamily: "sans-serif" }}>
      <h2>🤖 Chatbot con Voz</h2>
      <div style={{ border: "1px solid #ccc", padding: 10, height: 300, overflowY: "auto" }}>
        {messages.map((msg, i) => (
          <div key={i} style={{ textAlign: msg.from === "user" ? "right" : "left", margin: "5px 0" }}>
            <strong>{msg.from === "user" ? "Tú" : "Bot"}:</strong> {msg.text}
          </div>
        ))}
      </div>
      <input
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={(e) => e.key === "Enter" && sendMessage(input)}
        placeholder="Escribe o usa el micrófono..."
        style={{ width: "75%", padding: 10, marginTop: 10 }}
      />
      <button onClick={() => sendMessage(input)} style={{ marginLeft: 10, padding: 10 }}>Enviar</button>
      <button onClick={handleVoiceInput} style={{ marginLeft: 10, padding: 10 }}>🎤 Hablar</button>
    </div>
  );
}

export default App;
