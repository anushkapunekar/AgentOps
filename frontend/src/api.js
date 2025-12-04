const BACKEND = import.meta.env.VITE_BACKEND_URL || "http://localhost:8000";

export async function checkSession() {
  try {
    const token = localStorage.getItem("agentops_session_token");
    if (!token) return null;
    const r = await fetch(`${BACKEND}/mr/overview`, { headers: { Authorization: `Bearer ${token}` } });
    if (r.ok) return await r.json();
    // invalid session -> clear
    localStorage.removeItem("agentops_session_token");
  } catch (e) {
    console.error("session check failed", e);
  }
  return null;
}

export function startLogin() {
  window.location.href = `${BACKEND}/auth/login`;
}

export async function listProjects() {
  const token = localStorage.getItem("agentops_session_token");
  const r = await fetch(`${BACKEND}/install/projects`, { headers: { Authorization: `Bearer ${token}` } });
  if (!r.ok) throw new Error("Failed to list projects");
  return r.json();
}

export async function installProject(projectId) {
  const token = localStorage.getItem("agentops_session_token");
  const r = await fetch(`${BACKEND}/install/projects/${projectId}/install`, {
    method: "POST",
    headers: { Authorization: `Bearer ${token}`, "Content-Type": "application/json" }
  });
  if (!r.ok) {
    const text = await r.text();
    throw new Error("Install failed: " + text);
  }
  return r.json();
}
