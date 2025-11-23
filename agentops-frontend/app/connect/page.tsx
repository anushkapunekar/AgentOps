"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { api } from "@/lib/api";

export default function ConnectPage() {
  const [token, setToken] = useState("");
  const [baseUrl, setBaseUrl] = useState("");

  async function save() {
    await api.post("/save-settings", {
      token,
      base_url: baseUrl
    });
    alert("GitLab Connected!");
  }

  return (
    <div className="max-w-md mx-auto mt-20 space-y-6">
      <h1 className="text-3xl font-bold">Connect GitLab</h1>
      <Input
        placeholder="GitLab Token"
        value={token}
        onChange={(e) => setToken(e.target.value)}
      />
      <Input
        placeholder="GitLab Base URL"
        value={baseUrl}
        onChange={(e) => setBaseUrl(e.target.value)}
      />
      <Button onClick={save}>Save</Button>
    </div>
  );
}
