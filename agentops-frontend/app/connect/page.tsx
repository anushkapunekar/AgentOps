"use client";

import { motion } from "framer-motion";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { api } from "@/lib/api";
import { useState } from "react";

export default function ConnectPage() {
  const [gitlabUrl, setGitlabUrl] = useState("");
  const [token, setToken] = useState("");

  async function handleConnect() {
    try {
      await api.post("/save-settings", {
        gitlab_url: gitlabUrl,
        token,
      });

      window.location.href = "/dashboard";
    } catch {
      alert("Connection failed");
    }
  }

  return (
    <motion.div
      className="max-w-lg mx-auto pt-32 space-y-6"
      initial={{ opacity: 0, y: 30 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6 }}
    >
      <h1 className="text-4xl font-semibold">Connect GitLab</h1>

      <Input
        placeholder="Enter GitLab URL…"
        value={gitlabUrl}
        onChange={(e) => setGitlabUrl(e.target.value)}
      />

      <Input
        placeholder="Enter Personal Access Token…"
        value={token}
        onChange={(e) => setToken(e.target.value)}
      />

      <Button onClick={handleConnect}>Connect</Button>
    </motion.div>
  );
}
