"use client";

import { motion } from "framer-motion";
import { useEffect, useState } from "react";
import { Button } from "@/components/ui/button";

export default function Onboarding() {
  const [text, setText] = useState("");
  const fullText = "Initializing AgentOps… Booting AI reviewer… Linking neural modules…";

  useEffect(() => {
    let index = 0;
    const interval = setInterval(() => {
      setText(fullText.slice(0, index));
      index++;
      if (index > fullText.length) clearInterval(interval);
    }, 40);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="min-h-screen flex flex-col items-center justify-center relative overflow-hidden">

      {/* Neon glowing orbs */}
      <div className="absolute top-20 left-20 w-64 h-64 bg-purple-500/40 rounded-full ai-orb"></div>
      <div className="absolute bottom-20 right-20 w-64 h-64 bg-blue-500/40 rounded-full ai-orb"></div>

      {/* Content */}
      <motion.div
        initial={{ opacity: 0, y: 40 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 1 }}
        className="text-center space-y-8 z-10"
      >
        <h1 className="text-6xl font-bold neon-text">AgentOps</h1>

        <p className="text-xl text-white/70 min-h-[50px]">
          {text}
        </p>

        <Button
          className="mt-6 neon-glow"
          onClick={() => window.location.href = "/connect"}
        >
          Continue
        </Button>
      </motion.div>
    </div>
  );
}
