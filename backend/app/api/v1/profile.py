import time
from typing import Dict, Optional
import httpx
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/profile", tags=["Profile"])

class ProfileResponse(BaseModel):
    handle: str
    rating: Optional[int] = None
    maxRating: Optional[int] = None
    rank: Optional[str] = None
    maxRank: Optional[str] = None
    contribution: Optional[int] = None
    friendOfCount: Optional[int] = None

# Simple in-memory cache: {handle: (timestamp, profile_data)}
profile_cache: Dict[str, tuple[float, dict]] = {}
CACHE_TTL = 60  # seconds

@router.get("/{handle}", response_model=ProfileResponse)
async def get_profile(handle: str):
    current_time = time.time()
    
    # Check cache
    if handle in profile_cache:
        timestamp, data = profile_cache[handle]
        if current_time - timestamp < CACHE_TTL:
            return data

    url = f"https://codeforces.com/api/user.info?handles={handle}"

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, timeout=10.0)
            response.raise_for_status()
        except httpx.RequestError as exc:
            raise HTTPException(status_code=503, detail=f"Request to Codeforces API failed: {str(exc)}")
        except httpx.HTTPStatusError as exc:
            raise HTTPException(
                status_code=exc.response.status_code,
                detail=f"Codeforces API returned an error: {exc.response.status_code}"
            )

    data = response.json()
    if data.get("status") != "OK":
        error_msg = data.get("comment", "Unknown error from Codeforces API")
        raise HTTPException(status_code=400, detail=error_msg)
        
    result = data.get("result", [])
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
        
    user_info = result[0]
    profile_data = {
        "handle": user_info.get("handle"),
        "rating": user_info.get("rating"),
        "maxRating": user_info.get("maxRating"),
        "rank": user_info.get("rank"),
        "maxRank": user_info.get("maxRank"),
        "contribution": user_info.get("contribution"),
        "friendOfCount": user_info.get("friendOfCount"),
    }
    
    # Update cache
    profile_cache[handle] = (current_time, profile_data)
    
    return profile_data
