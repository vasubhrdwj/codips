"use client";
import { useState, useEffect } from "react";
import { getRank, isFallenGeneral } from "@/lib/ranks";

type Profile = {
  handle: string;
  rating: number | null;
  maxRating: number | null;
  rank: string | null;
  maxRank: string | null;
  contribution: number | null;
  friendOfCount: number | null;
};

export default function ProfileCard({ profile }: { profile: Profile }) {
  const rank = getRank(profile.rating);
  const fallen = isFallenGeneral(profile.rating, profile.maxRating);
  const ratingPercent = Math.round(((profile.rating || 0) / 3500) * 100);
  const targetImageSrc = `/${rank.title.toLowerCase().replace(/\s+/g, '-')}.png`;
  const [currentImage, setCurrentImage] = useState(targetImageSrc);
  const [emoji, setEmoji] = useState("⚔️");

  useEffect(() => {
    setCurrentImage(targetImageSrc);
  }, [targetImageSrc]);

  useEffect(() => {
    const fetchEmoji = async () => {
      try {
        const res = await fetch(`http://localhost:8000/api/v1/rank/${profile.rating || 0}`);
        if (res.ok) {
          const data = await res.json();
          setEmoji(data.emoji);
        }
      } catch (e) {
        console.error("Failed to fetch emoji", e);
      }
    };
    fetchEmoji();
  }, [profile.rating]);

  return (
    <div className="flex gap-6 items-stretch max-w-full overflow-x-auto p-4 shrink-0">
      <div className="w-[440px] bg-zinc-950 border border-zinc-800 relative overflow-hidden font-mono shrink-0">

      {/* Header */}
      <div className="px-6 py-5 border-b border-zinc-800 flex items-center gap-4">
        <div className="relative">
          <div className="w-14 h-14 bg-zinc-900 border-2 border-blue-500 flex items-center justify-center text-2xl">
            {emoji}
          </div>
          {/* <span className="absolute -bottom-1 -right-1 bg-blue-500 text-white text-[9px] font-bold px-1.5 py-0.5 uppercase tracking-wider">
            {profile.rank || "UNRATED"}
          </span> */}
        </div>
        <div>
          <h2 className="text-xl font-bold text-zinc-100 tracking-tight">
            <span className="text-blue-400">#</span>{profile.handle}
          </h2>
          <p className="text-[11px] text-blue-400 uppercase tracking-widest mt-0.5">
            ▸ Competitive Programmer
          </p>
        </div>
      </div>

      {/* Rating */}
      <div className="px-6 py-4 border-b border-zinc-800">
        <p className="text-[10px] text-zinc-600 uppercase tracking-widest mb-2">// Combat Rating</p>
        <div className="flex items-end gap-3 mb-3">
          <span className="text-5xl font-bold text-blue-400 leading-none">
            {profile.rating || 0}
          </span>
          <span className="text-xs text-zinc-500 pb-1">
            Peak: <span className="text-zinc-300">{profile.maxRating || 0}</span>
          </span>
        </div>
        <div className="h-1 bg-zinc-900">
          <div
            className="h-full bg-gradient-to-r from-blue-900 to-blue-400 transition-all duration-1000"
            style={{ width: `${Math.min(ratingPercent, 100)}%` }}
          />
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-2">
        {[
          { label: "Max Rating", value: profile.maxRating || 0, color: "" },
          { label: "Max Rank", value: profile.maxRank || "N/A", color: "" },
          {
            label: "Contribution",
            value: profile.contribution !== null ? (profile.contribution > 0 ? `+${profile.contribution}` : profile.contribution) : 0,
            color: profile.contribution !== null ? (profile.contribution >= 0 ? "text-emerald-400" : "text-red-400") : "text-emerald-400",
          },
          { label: "Allies", value: profile.friendOfCount || 0, color: "" },
        ].map((stat, i) => (
          <div
            key={i}
            className={`px-6 py-3 border-zinc-800 ${i % 2 === 0 ? "border-r" : ""} ${i >= 2 ? "border-t" : ""}`}
          >
            <p className={`text-2xl font-bold ${stat.color || "text-zinc-200"}`}>
              {stat.value}
            </p>
            <p className="text-[10px] text-zinc-600 uppercase tracking-widest mt-1">
              {stat.label}
            </p>
          </div>
        ))}
      </div>

      {/* Footer */}
      <div className="px-6 py-3 flex items-center justify-between border-t border-zinc-800">
        <div className="flex items-center gap-2">
          <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
          <span className="text-[10px] text-zinc-600 tracking-widest uppercase">Active · Codeforces</span>
        </div>
        <span className="text-[10px] text-zinc-700">CF/{profile.handle}</span>
      </div>
      </div>

      {/* Dynamic Rank Image Box */}
      <div className="w-[440px] bg-zinc-950/30 border border-zinc-800 relative overflow-hidden font-mono flex shrink-0 items-center justify-center p-2">
        <picture>
          {/* As a bulletproof fallback before hydration, we load raw-conscript natively if primary fails */}
          <img 
            ref={(img) => {
              if (img && img.complete && img.naturalHeight === 0 && currentImage !== "/raw-conscript.png") {
                setCurrentImage("/raw-conscript.png");
              }
            }}
            src={currentImage} 
            alt={rank.title} 
            className="max-w-full max-h-full object-contain drop-shadow-2xl opacity-90 hover:opacity-100 transition-opacity"
            onError={() => {
              if (currentImage !== "/raw-conscript.png") {
                setCurrentImage("/raw-conscript.png");
              }
            }}
          />
        </picture>
      </div>
    </div>
  );
}
