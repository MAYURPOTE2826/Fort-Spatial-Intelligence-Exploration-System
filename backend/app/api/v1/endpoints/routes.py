from fastapi import APIRouter
from typing import Any

router = APIRouter()

@router.get("/")
def get_routes() -> Any:
    """Get trekking routes."""
    # Placeholder
    return []

@router.get("/{route_id}")
def get_route(route_id: int) -> Any:
    """Get trekking route by ID."""
    # Placeholder
    return {"id": route_id, "name": "Dummy Route"}
