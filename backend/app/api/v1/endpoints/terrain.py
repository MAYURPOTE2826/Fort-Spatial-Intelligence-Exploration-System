from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Any
from app.core.database import get_db
from app.services.terrain_service import TerrainService

router = APIRouter()

@router.get("/elevation")
def get_elevation(
    lat: float, 
    lon: float, 
    db: Session = Depends(get_db)
) -> Any:
    """Get elevation at a specific point."""
    return TerrainService._get_elevation_from_cache(db, lat, lon)
