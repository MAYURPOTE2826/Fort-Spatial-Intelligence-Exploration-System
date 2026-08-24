from fastapi import APIRouter
from app.core.config import settings

router = APIRouter()

@router.get("/health")
def health_check():
    """Basic health check endpoint."""
    return {"status": "ok", "message": f"{settings.PROJECT_NAME} Backend is running"}

@router.get("/ready")
def readiness_check():
    """Readiness check endpoint (e.g. check DB connection)."""
    # TODO: Implement actual DB check if needed
    return {"status": "ok", "ready": True}
