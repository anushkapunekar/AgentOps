import React, { useEffect, useState } from "react";
import { checkSession, startLogin } from "./api";
import Connect from "./pages/Connect";
import Overview from "./pages/Overview";
import Projects from "./pages/Projects";

export default function App() {
  const [connected, setConnected] = useState(false);
  const [overviewData, setOverviewData] = useState([]);

  useEffect(() => {
    async function init() {
      const s = await checkSession();
      if (s && s.items) {
        setConnected(true);
        setOverviewData(s.items);
      } else {
        setConnected(false);
      }
    }
    init();
  }, []);

  if (!connected) {
    return <Connect onLogin={() => startLogin()} />;
  }

  return (
    <div>
      <div style={{ padding: 12, borderBottom: "1px solid #eee" }}>
        <button onClick={() => (window.location.href = "/")}>Overview</button>{" "}
        <button onClick={() => (window.location.href = "/projects")}>Install</button>
        <button onClick={() => { localStorage.removeItem("agentops_session_token"); window.location.reload(); }}>Logout</button>
      </div>
      {window.location.pathname === "/projects" ? (
        <Projects />
      ) : (
        <Overview items={overviewData} />
      )}
    </div>
  );
}
