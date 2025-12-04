"use client";

import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { api } from "@/lib/api";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { ArrowUpRight, CheckCircle2, Clock, XCircle } from "lucide-react";

type ReviewStatus = "reviewed" | "pending" | "failed";

interface ReviewItem {
  id: string;
  mr_iid: number;
  title: string;
  branch: string;
  status: ReviewStatus;
  summary: string;
  url?: string;
  created_at?: string;
}

const statusStyles: Record<ReviewStatus, string> = {
  reviewed: "bg-emerald-500/15 text-emerald-300 border border-emerald-500/40",
  pending: "bg-amber-500/15 text-amber-300 border border-amber-500/40",
  failed: "bg-red-500/15 text-red-300 border border-red-500/40",
};

const statusLabel: Record<ReviewStatus, string> = {
  reviewed: "Reviewed",
  pending: "Pending",
  failed: "Failed",
};

const statusIcon: Record<ReviewStatus, JSX.Element> = {
  reviewed: <CheckCircle2 className="w-4 h-4" />,
  pending: <Clock className="w-4 h-4" />,
  failed: <XCircle className="w-4 h-4" />,
};

export default function ReviewsPage() {
  const [reviews, setReviews] = useState<ReviewItem[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchReviews();
  }, []);

  async function fetchReviews() {
    try {
      // Try to call backend endpoint
      const res = await api.get("/reviews");
      setReviews(res.data.reviews || []);
    } catch (e) {
      console.log("No /reviews endpoint yet – using mock data for now.");

      // Fallback mock data so UI still works
      setReviews([
        {
          id: "1",
          mr_iid: 12,
          title: "Refactor webhook handler",
          branch: "feature/webhook-refactor",
          status: "reviewed",
          summary: "Cleaned up async logging, added background task for AI review.",
          url: "",
          created_at: "2025-12-04T10:30:00Z",
        },
        {
          id: "2",
          mr_iid: 15,
          title: "Add AgentOps Groq pipeline",
          branch: "feature/groq-agent",
          status: "pending",
          summary: "Initial version of Groq-based AI reviewer. Awaiting comments…",
          url: "",
          created_at: "2025-12-04T11:10:00Z",
        },
        {
          id: "3",
          mr_iid: 9,
          title: "Fix GitLab diff edge cases",
          branch: "bugfix/mr-diff",
          status: "failed",
          summary: "Review failed due to invalid diff payload from GitLab.",
          url: "",
          created_at: "2025-12-03T16:45:00Z",
        },
      ]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <motion.div
      className="p-10 max-w-5xl mx-auto space-y-8"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
    >
      <div className="flex items-center justify-between gap-4">
        <div>
          <h1 className="text-4xl font-semibold">Active Reviews</h1>
          <p className="text-white/60 mt-1">
            Recent merge requests processed by your AgentOps reviewer.
          </p>
        </div>
        <Button onClick={fetchReviews} className="neon-glow">
          Refresh
        </Button>
      </div>

      <Card className="overflow-hidden border border-white/10">
        <div className="grid grid-cols-12 px-4 py-3 text-xs uppercase tracking-wide text-white/50 border-b border-white/5">
          <div className="col-span-4">Merge Request</div>
          <div className="col-span-2">Branch</div>
          <div className="col-span-2">Status</div>
          <div className="col-span-3">Summary</div>
          <div className="col-span-1 text-right">Open</div>
        </div>

        {loading ? (
          <div className="p-6 text-white/60 text-sm">Loading reviews…</div>
        ) : reviews.length === 0 ? (
          <div className="p-6 text-white/60 text-sm">
            No reviews yet. Create a merge request in your connected GitLab project to see it here.
          </div>
        ) : (
          <div className="divide-y divide-white/5">
            {reviews.map((r) => (
              <div
                key={r.id}
                className="grid grid-cols-12 px-4 py-4 text-sm items-center hover:bg-white/5 transition"
              >
                {/* MR title + IID */}
                <div className="col-span-4 pr-4">
                  <div className="font-medium text-white">
                    !{r.mr_iid} – {r.title}
                  </div>
                  <div className="text-xs text-white/50">
                    {r.created_at ? new Date(r.created_at).toLocaleString() : ""}
                  </div>
                </div>

                {/* Branch */}
                <div className="col-span-2 text-white/70 text-xs">
                  <span className="px-2 py-1 rounded-md bg-white/5 border border-white/10">
                    {r.branch}
                  </span>
                </div>

                {/* Status badge */}
                <div className="col-span-2">
                  <span
                    className={
                      "inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs " +
                      statusStyles[r.status]
                    }
                  >
                    {statusIcon[r.status]}
                    {statusLabel[r.status]}
                  </span>
                </div>

                {/* Summary preview */}
                <div className="col-span-3 pr-4 text-white/70 text-xs line-clamp-2">
                  {r.summary}
                </div>

                {/* Open MR button */}
                <div className="col-span-1 text-right">
                  {r.url ? (
                    <a
                      href={r.url}
                      target="_blank"
                      rel="noreferrer"
                      className="inline-flex items-center justify-end text-xs text-white/70 hover:text-white"
                    >
                      <ArrowUpRight className="w-4 h-4" />
                    </a>
                  ) : (
                    <span className="text-xs text-white/30">—</span>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </Card>
    </motion.div>
  );
}
