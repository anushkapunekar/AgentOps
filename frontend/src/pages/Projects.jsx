import React, { useEffect, useState } from "react";
import { listProjects, installProject } from "../api";

export default function Projects() {
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [installing, setInstalling] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function load() {
      setLoading(true);
      try {
        const res = await listProjects();
        setProjects(res.projects || []);
      } catch (e) {
        setError(e.message);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  async function onInstall(projectId) {
    setInstalling(projectId);
    setError(null);
    try {
      const res = await installProject(projectId);
      alert("Installed! Installation ID: " + res.installation_id);
    } catch (e) {
      setError(String(e));
    } finally {
      setInstalling(null);
    }
  }

  if (loading) return <div style={{ padding: 20 }}>Loading projects…</div>;
  if (error) return <div style={{ padding: 20, color: "red" }}>Error: {error}</div>;

  return (
    <div style={{ padding: 20 }}>
      <h2>Your GitLab Projects</h2>
      {projects.length === 0 && <div>No projects available.</div>}
      {projects.map((p) => (
        <div key={p.id} style={{ marginBottom: 12, border: "1px solid #eee", padding: 12 }}>
          <div style={{ fontWeight: 600 }}>{p.name}</div>
          <div style={{ fontSize: 12, color: "#666" }}>{p.visibility}</div>
          <button disabled={installing === p.id} onClick={() => onInstall(p.id)} style={{ marginTop: 8 }}>
            {installing === p.id ? "Installing…" : "Install Agent"}
          </button>
        </div>
      ))}
    </div>
  );
}
