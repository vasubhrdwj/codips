from fastapi import APIRouter
from app.api.v1 import profile, rank

api_router = APIRouter()
api_router.include_router(profile.router)
api_router.include_router(rank.router)

# Register future routers here:
# from app.api.v1 import users
# api_router.include_router(users.router)
