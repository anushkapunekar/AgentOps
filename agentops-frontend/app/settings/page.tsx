"use client";

import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { api } from "@/lib/api";
import { Link2, Cog, KeyRound, GitBranch } from "lucide-react";

export default function SettingsPage() {
  const [settings, setSettings] = useState<any>(null);

  useEffect(() => {
    fetchSettings();
  }, []);

  async function fetchSettings() {
    try {
      const res = await api.get("/get-settings");
      setSettings(res.data);
    } catch {
      console.log("Could not fetch settings.");
    }
  }

  return (
    <motion.div
      className="p-10 space-y-10 max-w-4xl mx-auto"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
    >
      <h1 className="text-4xl font-semibold flex items-center gap-3">
        <Cog className="text-white/70" /> Settings
      </h1>

      {/* GitLab Connection Panel */}
      <Card className="space-y-4">
        <div className="flex items-center gap-3">
          <Link2 className="text-purple-400" />
          <h2 className="text-xl font-semibold">GitLab Integration</h2>
        </div>

        <p className="text-white/60">
          Status:{" "}
          <span className="text-purple-300 font-medium">
            {settings?.gitlab_url ? "Connected" : "Not Connected"}
          </span>
        </p>

        <p className="text-white/60 break-all">
          GitLab URL:
          <span className="text-white ml-2">{settings?.gitlab_url || "—"}</span>
        </p>

        <Button
          onClick={() => (window.location.href = "/connect")}
          className="neon-glow"
        >
          Reconnect GitLab
        </Button>
      </Card>

      {/* Token Panel */}
      <Card className="space-y-4">
        <div className="flex items-center gap-3">
          <KeyRound className="text-blue-400" />
          <h2 className="text-xl font-semibold">Credentials</h2>
        </div>

        <p className="text-white/60">
          Token Status:{" "}
          <span className="text-blue-300 font-medium">
            {settings?.token ? "Saved" : "Missing"}
          </span>
        </p>
      </Card>

      {/* Project Panel */}
      <Card className="space-y-4">
        <div className="flex items-center gap-3">
          <GitBranch className="text-green-400" />
          <h2 className="text-xl font-semibold">Project Info</h2>
        </div>

        <p className="text-white/60">
          Project ID:
          <span className="text-green-300 ml-2">
            {settings?.project_id || "Not Set"}
          </span>
        </p>

        <p className="text-white/60">
          Webhook Status:
          <span className="text-green-300 ml-2">
            {settings?.webhook_status || "Unknown"}
          </span>
        </p>
      </Card>

    </motion.div>
  );
}
