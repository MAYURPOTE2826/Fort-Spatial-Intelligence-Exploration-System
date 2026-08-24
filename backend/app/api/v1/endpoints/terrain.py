from fastapi import APIRouter
from typing import Any

router = APIRouter()

@router.get("/elevation")
def get_elevation(lat: float, lon: float) -> Any:
    """Get elevation at a specific point."""
    # Placeholder
    return {"lat": lat, "lon": lon, "elevation": 0.0}
