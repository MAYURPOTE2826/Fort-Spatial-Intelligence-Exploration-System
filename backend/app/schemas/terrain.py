from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, Any

class TerrainTileBase(BaseModel):
    tile_name: str
    zoom_level: int
    file_path: str
    resolution_m: Optional[float] = None

class TerrainTileCreate(TerrainTileBase):
    geometry_wkt: str

class TerrainTileUpdate(BaseModel):
    tile_name: Optional[str] = None
    zoom_level: Optional[int] = None
    file_path: Optional[str] = None
    resolution_m: Optional[float] = None
    geometry_wkt: Optional[str] = None

class TerrainTileInDB(TerrainTileBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class TerrainTileResponse(TerrainTileInDB):
    geometry: Optional[Dict[str, Any]] = None
