"use client";

import { useEffect } from "react";

export default function Home() {
  useEffect(() => {
    const first = localStorage.getItem("first-time");
    if (!first) {
      localStorage.setItem("first-time", "done");
      window.location.href = "/onboarding";
    } else {
      window.location.href = "/dashboard";
    }
  }, []);

  return null;
}
