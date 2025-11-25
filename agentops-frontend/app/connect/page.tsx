"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { api } from "@/lib/api";

export default function ConnectPage() {
  const [token, setToken] = useState("");
  const [baseUrl, setBaseUrl] = useState("https://gitlab.com");
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  async function handleConnect() {
    setLoading(true);
    setSuccess(null);
    setError(null);

    try {
      const res = await api.post("/validate-token", {
        token,
        base_url: baseUrl,
      });

      const data = res.data;
      const displayName = data.name || data.username || "GitLab user";

      setSuccess(`Connected successfully as ${displayName}.`);
      // later we can also call /save-settings here
    } catch (err: any) {
      const message =
        err?.response?.data?.detail || "Failed to validate token. Please check your details.";
      setError(message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="max-w-md mx-auto mt-20 space-y-6">
      <h1 className="text-3xl font-bold">Connect GitLab</h1>
      <p className="text-sm text-muted-foreground">
        Enter your GitLab Personal Access Token and instance URL to connect AgentOps.
      </p>

      <div className="space-y-3">
        <div>
          <label className="text-sm font-medium">GitLab Base URL</label>
          <Input
            placeholder="https://gitlab.com"
            value={baseUrl}
            onChange={(e) => setBaseUrl(e.target.value)}
          />
        </div>

        <div>
          <label className="text-sm font-medium">GitLab Personal Access Token</label>
          <Input
            placeholder="glpat-..."
            value={token}
            onChange={(e) => setToken(e.target.value)}
          />
        </div>
      </div>

      <Button onClick={handleConnect} disabled={loading || !token || !baseUrl}>
        {loading ? "Connecting..." : "Connect"}
      </Button>

      {success && <p className="text-sm text-green-600 mt-2">{success}</p>}
      {error && <p className="text-sm text-red-600 mt-2">{error}</p>}
    </div>
  );
}
