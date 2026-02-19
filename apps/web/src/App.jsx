import { useMemo, useState } from "react";
import "./App.css";

const API_BASE = "http://127.0.0.1:8000";

export default function App() {
  const endpoints = useMemo(
    () => [
      { key: "services", label: "Service Registry", path: "/services" },
      { key: "envs", label: "Environments", path: "/environments" },
      { key: "deployments", label: "Deployments", path: "/deployments" },
      { key: "runbooks", label: "Runbooks", path: "/runbooks" },
      { key: "incidents", label: "Incidents", path: "/incidents" },
      { key: "audit", label: "Audit Log", path: "/audit/events" },
      { key: "obs", label: "Observability Links", path: "/observability/links" },
      { key: "health", label: "Health", path: "/health" },
    ],
    []
  );

  const [activeKey, setActiveKey] = useState(endpoints[0].key);
  const [loading, setLoading] = useState(false);
  const [statusLine, setStatusLine] = useState("");
  const [data, setData] = useState(null);

  const active = endpoints.find((e) => e.key === activeKey);

  async function fetchActive() {
    setLoading(true);
    setStatusLine("");
    setData(null);

    try {
      const url = `${API_BASE}${active.path}`;
      const res = await fetch(url);

      setStatusLine(`${res.status} ${res.statusText}`);

      const text = await res.text();
      // handle JSON or plain text
      try {
        setData(JSON.parse(text));
      } catch {
        setData(text);
      }
    } catch (e) {
      setStatusLine("ERROR");
      setData(`Failed to fetch: ${e.message}`);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="appShell">
      <aside className="sidebar">
        <div className="brand">
          <div className="brandDot" />
          <div>
            <div className="brandTitle">ChalkOps</div>
            <div className="brandSub">Local Console</div>
          </div>
        </div>

        <nav className="nav">
          {endpoints.map((e) => (
            <button
              key={e.key}
              className={`navItem ${e.key === activeKey ? "active" : ""}`}
              onClick={() => setActiveKey(e.key)}
              type="button"
            >
              {e.label}
              <span className="navPath">{e.path}</span>
            </button>
          ))}
        </nav>

        <div className="sidebarFooter">
          <div className="muted">API</div>
          <div className="mono">{API_BASE}</div>
        </div>
      </aside>

      <main className="main">
        <div className="panel">
          <div className="panelHeader">
            <div>
              <div className="panelTitle">{active.label}</div>
              <div className="panelSub mono">
                GET {active.path}
                {statusLine ? `  •  ${statusLine}` : ""}
              </div>
            </div>

            <button
              className="primaryBtn"
              onClick={fetchActive}
              type="button"
              disabled={loading}
            >
              {loading ? "Loading..." : "Fetch"}
            </button>
          </div>

          <div className="codeBox">
            <pre className="codePre">
              {data === null
                ? "Click Fetch to call the API."
                : typeof data === "string"
                ? data
                : JSON.stringify(data, null, 2)}
            </pre>
          </div>
        </div>
      </main>
    </div>
  );
}
