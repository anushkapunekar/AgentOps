"use client";

import { motion } from "framer-motion";
import { Card } from "@/components/ui/card";

export default function Dashboard() {
  return (
    <motion.div
      className="p-10 space-y-6"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6, ease: "easeOut" }}
    >
      <h1 className="text-5xl font-semibold">Dashboard</h1>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <motion.div
          whileHover={{ scale: 1.02 }}
          transition={{ type: "spring", stiffness: 120 }}
        >
          <Card>
            <p className="text-xl font-semibold">Status</p>
            <p className="text-white/70">Connected & Running</p>
          </Card>
        </motion.div>

        <motion.div whileHover={{ scale: 1.02 }}>
          <Card>
            <p className="text-xl font-semibold">Reviews</p>
            <p className="text-white/70">AI reviewing enabled</p>
          </Card>
        </motion.div>

        <motion.div whileHover={{ scale: 1.02 }}>
          <Card>
            <p className="text-xl font-semibold">Pipeline</p>
            <p className="text-white/70">Auto-triggered</p>
          </Card>
        </motion.div>
      </div>
    </motion.div>
  );
}
