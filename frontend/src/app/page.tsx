"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";

export default function Dashboard() {
  const [handle, setHandle] = useState("");
  const [error, setError] = useState("");
  const router = useRouter();

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    const trimmed = handle.trim();
    if (!trimmed) {
      setError("Enter a Codeforces handle");
      return;
    }
    router.push(`/profile/${trimmed}`);
  }

  return (
    <main className="min-h-screen bg-zinc-950 flex flex-col items-center justify-center gap-8">
      
      <div className="text-center">
        <h1 className="text-4xl font-bold text-zinc-100 tracking-tight">
          ⚔️ CF<span className="text-blue-400">Rank</span>
        </h1>
        <p className="text-zinc-500 text-sm mt-2 font-mono tracking-widest uppercase">
          Enter your handle. Know your rank.
        </p>
      </div>

      <form onSubmit={handleSubmit} className="flex flex-col gap-3 w-full max-w-sm px-4">
        <div className="flex gap-2">
          <Input
            placeholder="e.g. IffyNeuron"
            value={handle}
            onChange={(e) => {
              setHandle(e.target.value);
              setError("");
            }}
            className="bg-zinc-900 border-zinc-700 text-zinc-100 placeholder:text-zinc-600 font-mono"
          />
          <Button
            type="submit"
            className="bg-blue-600 hover:bg-blue-500 text-white font-bold tracking-wide"
          >
            Scout
          </Button>
        </div>
        {error && (
          <p className="text-red-400 text-xs font-mono tracking-wide">{error}</p>
        )}
      </form>

    </main>
  );
}
