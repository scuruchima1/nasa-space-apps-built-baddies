import { useState } from "react";

// Works with Vite (VITE_API_BASE) or CRA (REACT_APP_API_BASE)
const API_BASE = process.env.REACT_APP_API_BASE;

export default function ChatRunner() {
  const [loading, setLoading] = useState(false);
  const [text, setText] = useState("");
  const [err, setErr] = useState("");

const runChat = async () => {
  setLoading(true);
  setErr("");
  setText("");
  try {
    const res = await fetch(`http://localhost:5500/chat`, { method: "GET" });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);

    const { message, response } = await res.json();  // 👈 parse JSON
    setText(response || "(no text returned)");       // 👈 use the field you want
    console.log("message:", message);
  } catch (e) {
    setErr(e.message || "Request failed");
  } finally {
    setLoading(false);
  }
};


  return (
    <div style={box}>
      <h3 style={{ margin: 0 }}>Run /chat</h3>
      <p style={{ marginTop: 8, fontSize: 14, opacity: 0.8 }}>
        Click the button to call your Flask endpoint and display the model’s output.
      </p>
      <button onClick={runChat} disabled={loading} style={btn}>
        {loading ? "Running…" : "Run chat"}
      </button>

      {err && <p style={{ color: "tomato", marginTop: 12 }}>Error: {err}</p>}
      {text && (
        <pre style={pre}>
{text}
        </pre>
      )}
    </div>
  );
}

const box = { border: "1px solid #e5e7eb", borderRadius: 12, padding: 16, maxWidth: 640, fontFamily: "system-ui, sans-serif" };
const btn = { padding: "8px 12px", borderRadius: 8, border: "1px solid #111", background: "#fff", cursor: "pointer" };
const pre = { marginTop: 12, whiteSpace: "pre-wrap", background: "#fafafa", padding: 12, borderRadius: 8, border: "1px solid #eee" };
