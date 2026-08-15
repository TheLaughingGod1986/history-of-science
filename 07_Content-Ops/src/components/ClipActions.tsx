"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";

export function ClipActions({ clipId, status }: { clipId: string; status: string }) {
  const router = useRouter();
  const [busy, setBusy] = useState(false);

  async function setStatus(next: string) {
    setBusy(true);
    try {
      const res = await fetch(`/api/clips/${clipId}`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ status: next }),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error || "Failed");
      router.refresh();
    } catch (err) {
      alert(err instanceof Error ? err.message : "Failed");
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="flex flex-wrap gap-2">
      {status === "proposed" ? (
        <>
          <button
            disabled={busy}
            onClick={() => setStatus("approved")}
            className="inline-flex min-h-11 items-center rounded-full bg-[#FF7A24] px-4 py-2 text-sm text-[#0A0C12]"
          >
            Approve
          </button>
          <button
            disabled={busy}
            onClick={() => setStatus("rejected")}
            className="inline-flex min-h-11 items-center rounded-full border border-white/15 px-4 py-2 text-sm"
          >
            Reject
          </button>
        </>
      ) : null}
      {status === "approved" ? (
        <button
          disabled={busy}
          onClick={() => setStatus("editing")}
          className="inline-flex min-h-11 items-center rounded-full border border-white/15 px-4 py-2 text-sm"
        >
          Start editing
        </button>
      ) : null}
      {status === "editing" ? (
        <button
          disabled={busy}
          onClick={() => setStatus("exported")}
          className="inline-flex min-h-11 items-center rounded-full border border-white/15 px-4 py-2 text-sm"
        >
          Mark exported
        </button>
      ) : null}
    </div>
  );
}
