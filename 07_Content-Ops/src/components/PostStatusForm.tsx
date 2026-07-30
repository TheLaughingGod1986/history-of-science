"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";

export function PostStatusForm({
  postId,
  status,
  url,
}: {
  postId: string;
  status: string;
  url?: string | null;
}) {
  const router = useRouter();
  const [nextStatus, setNextStatus] = useState(status);
  const [platformUrl, setPlatformUrl] = useState(url || "");
  const [scheduledAt, setScheduledAt] = useState("");
  const [repostReason, setRepostReason] = useState("");
  const [msg, setMsg] = useState<string | null>(null);

  async function save() {
    setMsg(null);
    const res = await fetch(`/api/posts/${postId}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        uploadStatus: nextStatus,
        platformUrl: platformUrl || null,
        scheduledAt: scheduledAt || undefined,
        repostReason: repostReason || undefined,
      }),
    });
    const data = await res.json();
    if (!res.ok) {
      setMsg(data.error || "Failed");
      if (data.warnings) setMsg((data.error || "Duplicate warning") + " — " + data.warnings.map((w: { reason: string }) => w.reason).join("; "));
      return;
    }
    setMsg("Saved");
    router.refresh();
  }

  return (
    <div className="flex min-w-[240px] flex-col gap-2 text-xs">
      <select
        value={nextStatus}
        onChange={(e) => setNextStatus(e.target.value)}
        className="rounded-lg border border-white/10 bg-[#0A0C12] px-2 py-1.5"
      >
        {["draft", "ready", "scheduled", "published", "failed", "skipped"].map((s) => (
          <option key={s} value={s}>
            {s}
          </option>
        ))}
      </select>
      <input
        type="datetime-local"
        value={scheduledAt}
        onChange={(e) => setScheduledAt(e.target.value)}
        className="rounded-lg border border-white/10 bg-[#0A0C12] px-2 py-1.5"
      />
      <input
        placeholder="Published URL"
        value={platformUrl}
        onChange={(e) => setPlatformUrl(e.target.value)}
        className="rounded-lg border border-white/10 bg-[#0A0C12] px-2 py-1.5"
      />
      <select
        value={repostReason}
        onChange={(e) => setRepostReason(e.target.value)}
        className="rounded-lg border border-white/10 bg-[#0A0C12] px-2 py-1.5"
      >
        <option value="">Repost reason (if needed)</option>
        <option>New hook</option>
        <option>New edit</option>
        <option>Seasonal repost</option>
        <option>Performance retest</option>
        <option>Updated information</option>
      </select>
      <button onClick={save} className="rounded-full bg-white/10 px-3 py-1.5 hover:bg-white/15">
        Update
      </button>
      {msg ? <span className="text-[#FFC85A]">{msg}</span> : null}
    </div>
  );
}
