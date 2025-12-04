"use client";

import { motion } from "framer-motion";
import Link from "next/link";
import { Home, Link2, Settings } from "lucide-react";

export default function FloatingPanel() {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6 }}
      className="
        fixed bottom-8 left-1/2 -translate-x-1/2
        glass backdrop-blur-xl shadow-2xl
        px-6 py-3 rounded-2xl border border-white/10
        flex gap-8 z-50
      "
      className="
  fixed bottom-6 left-1/2 -translate-x-1/2
  glass px-5 py-2 rounded-2xl border border-white/10
  flex gap-6 z-50
  backdrop-blur-xl shadow-xl
  max-w-[90%]
  md:gap-8 md:px-6 md:py-3
"

    >
      {/* Home */}
      <Link href="/dashboard" className="group">
        <div className="flex flex-col items-center">
          <Home className="w-6 h-6 text-white/80 group-hover:text-white transition" />
          <span className="text-xs text-white/60 group-hover:text-white">Dashboard</span>
        </div>
      </Link>

      {/* Connect */}
      <Link href="/connect" className="group">
        <div className="flex flex-col items-center">
          <Link2 className="w-6 h-6 text-white/80 group-hover:text-white transition" />
          <span className="text-xs text-white/60 group-hover:text-white">Connect</span>
        </div>
      </Link>

      {/* Settings */}
      <Link href="/settings" className="group">
        <div className="flex flex-col items-center">
          <Settings className="w-6 h-6 text-white/80 group-hover:text-white transition" />
          <span className="text-xs text-white/60 group-hover:text-white">Settings</span>
        </div>
      </Link>
    </motion.div>
  );
}
