from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List, Dict, Any

class FortBase(BaseModel):
    name: str
    marathi_name: Optional[str] = None
    description: Optional[str] = None
    elevation: Optional[float] = None
    district: Optional[str] = None
    difficulty: Optional[str] = None
    best_season: Optional[str] = None
    history: Optional[str] = None
    image_url: Optional[str] = None
    source: Optional[str] = None

class FortCreate(FortBase):
    # Depending on how the API handles geometry, we can accept GeoJSON or WKT
    geometry_wkt: str

class FortUpdate(FortBase):
    geometry_wkt: Optional[str] = None

class FortInDB(FortBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class FortResponse(FortInDB):
    # In response, geometry might be parsed into GeoJSON dict
    geometry: Optional[Dict[str, Any]] = None

# FortViewpoint
class FortViewpointBase(BaseModel):
    name: str
    type: Optional[str] = None
    elevation: Optional[float] = None
    description: Optional[str] = None

class FortViewpointCreate(FortViewpointBase):
    fort_id: int
    geometry_wkt: str

class FortViewpointResponse(FortViewpointBase):
    id: int
    fort_id: int
    created_at: datetime
    geometry: Optional[Dict[str, Any]] = None

    class Config:
        from_attributes = True

# FortStructure
class FortStructureBase(BaseModel):
    name: str
    type: Optional[str] = None
    description: Optional[str] = None

class FortStructureCreate(FortStructureBase):
    fort_id: int
    geometry_wkt: str

class FortStructureResponse(FortStructureBase):
    id: int
    fort_id: int
    created_at: datetime
    geometry: Optional[Dict[str, Any]] = None

    class Config:
        from_attributes = True

# FortTrail
class FortTrailBase(BaseModel):
    name: str
    difficulty: Optional[str] = None
    distance_km: Optional[float] = None
    estimated_time_hours: Optional[float] = None

class FortTrailCreate(FortTrailBase):
    fort_id: int
    geometry_wkt: str

class FortTrailResponse(FortTrailBase):
    id: int
    fort_id: int
    created_at: datetime
    geometry: Optional[Dict[str, Any]] = None

    class Config:
        from_attributes = True

# FortConnection
class FortConnectionBase(BaseModel):
    source_fort_id: int
    target_fort_id: int
    distance_km: Optional[float] = None
    bearing_deg: Optional[float] = None
    visibility_status: Optional[str] = None
    visibility_score: Optional[float] = None

class FortConnectionCreate(FortConnectionBase):
    pass

class FortConnectionResponse(FortConnectionBase):
    last_calculated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Combined Response
class FortDetailResponse(FortResponse):
    viewpoints: List[FortViewpointResponse] = []
    structures: List[FortStructureResponse] = []
    trails: List[FortTrailResponse] = []
