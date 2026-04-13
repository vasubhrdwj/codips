from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/rank", tags=["Rank"])

class Rank(BaseModel):
    title: str
    emoji: str
    minRating: int
    maxRating: int
    color: str

RANKS = [
    { "title": "Raw Conscript",     "emoji": "🪨", "minRating": 0,    "maxRating": 399,  "color": "text-zinc-400" },
    { "title": "Foot Soldier",      "emoji": "🗡️",  "minRating": 400,  "maxRating": 799,  "color": "text-green-400" },
    { "title": "Archer",            "emoji": "🏹", "minRating": 800,  "maxRating": 1199, "color": "text-teal-400" },
    { "title": "Shield Guard",      "emoji": "🛡️",  "minRating": 1200, "maxRating": 1399, "color": "text-blue-400" },
    { "title": "Scout",             "emoji": "🗺️",  "minRating": 1400, "maxRating": 1599, "color": "text-cyan-400" },
    { "title": "Cavalry",           "emoji": "🐴", "minRating": 1600, "maxRating": 1899, "color": "text-violet-400" },
    { "title": "Sergeant",          "emoji": "⚔️",  "minRating": 1900, "maxRating": 2099, "color": "text-yellow-400" },
    { "title": "Lieutenant",        "emoji": "🎖️",  "minRating": 2100, "maxRating": 2299, "color": "text-orange-400" },
    { "title": "Major",             "emoji": "🔱", "minRating": 2300, "maxRating": 2399, "color": "text-red-400" },
    { "title": "Colonel",           "emoji": "🦅", "minRating": 2400, "maxRating": 2599, "color": "text-red-500" },
    { "title": "General",           "emoji": "🏴", "minRating": 2600, "maxRating": 2999, "color": "text-rose-400" },
    { "title": "High General",      "emoji": "👑", "minRating": 3000, "maxRating": 3199, "color": "text-amber-400" },
    { "title": "Supreme Commander", "emoji": "⚡", "minRating": 3200, "maxRating": 3499, "color": "text-amber-300" },
    { "title": "Eternal Marshal",   "emoji": "🌟", "minRating": 3500, "maxRating": 9999, "color": "text-yellow-200" },
]

@router.get("/{rating}", response_model=Rank)
async def get_rank(rating: int):
    for rank in RANKS:
        if rank["minRating"] <= rating <= rank["maxRating"]:
            return rank
    # If rating is extremely high or negative, handle gracefully
    if rating < 0:
        return RANKS[0]
    return RANKS[-1]
