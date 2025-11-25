"use client";

import { useState, useEffect } from "react";
import { api } from "@/lib/api";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

export default function DashboardPage() {
  const [repos, setRepos] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  async function enableWebhook(projectId: number) {
    try {
      const res = await api.post("/create-webhook", {
        token: "glpat-BC7jgIZhyeTTeNHid1GHUG86MQp1OmlncHkzCw.01.121ngjxmx",
        base_url: "https://gitlab.com",
        project_id: projectId,
        webhook_url: "https://agentops-2wff.onrender.com/webhook/gitlab"
      });

      if (res.data.ok) {
        alert("Webhook created!");
      } else {
        alert("GitLab error: " + res.data.message);
      }
    } catch (err: any) {
      alert("Error: " + (err.response?.data?.detail || "Unknown error"));
    }
  }

  useEffect(() => {
    api.post("/list-repos", {
      token: "glpat-BC7jgIZhyeTTeNHid1GHUG86MQp1OmlncHkzCw.01.121ngjxmx",
      base_url: "https://gitlab.com"
    })
      .then(res => {
        setRepos(res.data.projects);
      })
      .catch(err => {
        console.error("Failed to fetch repos:", err);
      })
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <p className="p-10">Loading repositories...</p>;

  return (
    <div className="p-10 space-y-6">
      <h1 className="text-3xl font-bold">Your GitLab Repositories</h1>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {repos.map(repo => (
          <Card key={repo.id} className="p-4 shadow-sm">
            <h2 className="font-semibold">{repo.name}</h2>
            <p className="text-sm text-muted-foreground">{repo.path}</p>

            <div className="mt-4">
              <Button
                onClick={() => enableWebhook(repo.id)}
                className="w-full"
              >
                Enable Reviewer
              </Button>
            </div>

            <a
              href={repo.web_url}
              target="_blank"
              className="text-blue-600 text-sm underline mt-3 inline-block"
            >
              Open on GitLab
            </a>
          </Card>
        ))}
      </div>
    </div>
  );
}
