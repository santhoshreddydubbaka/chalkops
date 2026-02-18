import { useState } from "react";
import "./App.css";

export default function App() {
  const [result, setResult] = useState("");

  async function pingApi() {
    setResult("Loading...");
    try {
      const res = await fetch("http://127.0.0.1:8000/health");
      const data = await res.json();
      setResult(JSON.stringify(data));
    } catch (e) {
      setResult("Error: " + e.message);
    }
  }

  return (
    <div style={{ padding: 24 }}>
      <h1>ChalkOps Web</h1>
      <button onClick={pingApi}>Ping API</button>
      <pre style={{ marginTop: 16 }}>{result}</pre>
    </div>
  );
}
