import { useEffect, useMemo, useState } from "react";
import axios from "axios";
import ReactMarkdown from "react-markdown";
import FileUpload from "./components/FileUpload";

export default function App() {
  const [prompt, setPrompt] = useState("");
  const [file, setFile] = useState(null);
  const [temperature, setTemperature] = useState(0.2);
  const [messages, setMessages] = useState([]);
  const [healthStatus, setHealthStatus] = useState("Checking API...");
  const [isSending, setIsSending] = useState(false);

  useEffect(() => {
    axios
      .get("/api/health")
      .then(() => setHealthStatus("API online"))
      .catch(() => setHealthStatus("API unavailable"));
  }, []);

  const canSend = useMemo(() => {
    return !isSending && (prompt.trim().length > 0 || file !== null);
  }, [file, isSending, prompt]);

  const apiOnline = healthStatus === "API online";

  async function handleSend(event) {
    event.preventDefault();
    if (!canSend) {
      return;
    }

    setIsSending(true);
    const userText = prompt.trim() || "[No prompt provided]";
    const userLine = file ? `${userText}\n\nAttached: ${file.name}` : userText;

    setMessages((prev) => [
      ...prev,
      { role: "user", content: userLine },
      { role: "assistant", content: "" }
    ]);

    const formData = new FormData();
    formData.append("prompt", prompt);
    formData.append("temperature", String(temperature));
    if (file) {
      formData.append("file", file);
    }

    let streamedText = "";
    try {
      const response = await axios.post("/api/chat", formData, {
        responseType: "text",
        onDownloadProgress: (progressEvent) => {
          const xhr = progressEvent.event?.currentTarget || progressEvent.event?.target;
          const partialText = xhr?.responseText;
          if (typeof partialText !== "string") {
            return;
          }
          streamedText = partialText;
          setMessages((prev) => {
            const next = [...prev];
            if (next.length > 0) {
              next[next.length - 1] = { role: "assistant", content: partialText };
            }
            return next;
          });
        }
      });

      const finalText = typeof response.data === "string" ? response.data : streamedText;
      setMessages((prev) => {
        const next = [...prev];
        if (next.length > 0) {
          next[next.length - 1] = { role: "assistant", content: finalText };
        }
        return next;
      });
    } catch (error) {
      const detail = error?.response?.data?.detail || error.message || "Unknown error";
      setMessages((prev) => {
        const next = [...prev];
        if (next.length > 0) {
          next[next.length - 1] = {
            role: "assistant",
            content: `Error: ${detail}`
          };
        }
        return next;
      });
    } finally {
      setPrompt("");
      setFile(null);
      setIsSending(false);
    }
  }

  return (
    <div className="app-bg">
      <div className="orb orb-a" />
      <div className="orb orb-b" />
      <div className="app-shell">
        <header className="topbar">
          <div className="brand">
            <p className="eyebrow">Workspace</p>
            <h1>Atlas Chat</h1>
          </div>
          <div className={`health-pill ${apiOnline ? "ok" : "warn"}`}>
            <span className="dot" />
            <span>{healthStatus}</span>
          </div>
        </header>

        <main className="chat-layout">
          <section className="thread-panel">
            <div className="panel-head">
              <p>Conversation</p>
              <small>{messages.length} messages</small>
            </div>
            <section className="messages">
              {messages.length === 0 ? (
                <div className="empty">
                  <h2>Ready when you are.</h2>
                  <p>Ask a question, attach a document, and stream a response in real time.</p>
                </div>
              ) : null}
              {messages.map((message, index) => (
                <article key={index} className={`message ${message.role}`}>
                  <div className="message-head">
                    <span className={`role-pill ${message.role}`}>
                      {message.role === "user" ? "You" : "Assistant"}
                    </span>
                  </div>
                  <div className="message-body">
                    {message.role === "assistant" ? (
                      <ReactMarkdown>{message.content}</ReactMarkdown>
                    ) : (
                      <p>{message.content}</p>
                    )}
                  </div>
                </article>
              ))}
            </section>
          </section>

          <aside className="composer-panel">
            <form className="composer" onSubmit={handleSend}>
              <div className="controls">
                <div className="stack-meta">
                  <span className="meta-label">Provider</span>
                  <span className="meta-value">xAI</span>
                </div>
                <label>
                  Temperature
                  <input
                    type="number"
                    min="0"
                    max="2"
                    step="0.1"
                    value={temperature}
                    onChange={(event) => setTemperature(Number(event.target.value))}
                  />
                </label>
              </div>

              <label className="prompt-wrap">
                Prompt
                <textarea
                  rows={8}
                  value={prompt}
                  onChange={(event) => setPrompt(event.target.value)}
                  placeholder="Ask something precise. You can also upload a supporting file."
                />
              </label>

              <div className="actions">
                <FileUpload file={file} onChange={setFile} />
                <button type="submit" disabled={!canSend}>
                  {isSending ? "Streaming..." : "Send Message"}
                </button>
              </div>
            </form>
          </aside>
        </main>
      </div>
    </div>
  );
}
