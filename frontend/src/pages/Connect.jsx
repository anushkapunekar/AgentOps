import React, { useEffect } from "react";

export default function Connect({ onLogin }) {
  useEffect(() => {
    // If redirected back from auth, store session token from URL param
    const params = new URLSearchParams(window.location.search);
    const session_token = params.get("session_token");
    if (session_token) {
      localStorage.setItem("agentops_session_token", session_token);
      // Remove param from URL
      window.history.replaceState({}, document.title, "/");
      // reload to let App detect connection
      window.location.href = "/";
    }
  }, []);

  return (
    <div style={{ padding: 20 }}>
      <h1>AgentOps — Connect your GitLab</h1>
      <p>Click below to connect your GitLab account and install the agent for a project.</p>
      <button onClick={onLogin} style={{ padding: "10px 16px", fontSize: 16 }}>
        Connect GitLab
      </button>
    </div>
  );
}
