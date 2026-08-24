from fastapi import APIRouter
from app.api.v1.endpoints import (
    health,
    forts,
    visibility,
    terrain,
    routes,
    chat,
    auth,
)

api_router = APIRouter()

api_router.include_router(health.router, tags=["health"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(forts.router, prefix="/forts", tags=["forts"])
api_router.include_router(visibility.router, prefix="/visibility", tags=["visibility"])
api_router.include_router(terrain.router, prefix="/terrain", tags=["terrain"])
api_router.include_router(routes.router, prefix="/routes", tags=["routes"])
api_router.include_router(chat.router, prefix="/chat", tags=["chat"])
