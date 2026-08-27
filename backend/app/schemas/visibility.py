from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List, Dict, Any

class ObserverInfo(BaseModel):
    lat: float
    lon: float
    elevation: Optional[float] = None
    heading: Optional[float] = None
    fov: Optional[float] = None
    radius_km: Optional[float] = None

class FortVisibilityItem(BaseModel):
    id: str
    name: str
    distance_km: float
    bearing_deg: float
    direction: str
    relative_angle: Optional[float] = None
    visibility_score: float
    visibility_status: str
    elevation: float
    elevation_difference: float
    image_url: Optional[str] = None
    obstruction_distance_km: Optional[float] = None
    confidence: Optional[float] = None
    explanation: Optional[str] = None

class VisibilityResponse(BaseModel):
    observer: ObserverInfo
    visible_forts: List[FortVisibilityItem] = []
    uncertain_forts: List[FortVisibilityItem] = []
    blocked_forts: List[FortVisibilityItem] = []
    calculation_time_ms: int

class BetweenFortsRequest(BaseModel):
    source_fort_id: str
    target_fort_id: str

class BuildNetworkRequest(BaseModel):
    fort_ids: List[str]
    
class NetworkVisibilityEdge(BaseModel):
    source_id: str
    target_id: str
    is_visible: bool
    distance_km: float
    visibility_score: float

class VisibilityNetworkResponse(BaseModel):
    nodes: List[str]
    edges: List[NetworkVisibilityEdge]
    calculation_time_ms: int
