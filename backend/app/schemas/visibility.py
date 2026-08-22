from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class VisibilityResultBase(BaseModel):
    observer_lat: float
    observer_lon: float
    observer_elevation: float
    visibility_status: str
    visibility_score: float

class VisibilityResultCreate(VisibilityResultBase):
    fort_id: int
    expires_at: datetime

class VisibilityResultResponse(VisibilityResultBase):
    id: int
    fort_id: int
    calculated_at: datetime
    expires_at: datetime

    class Config:
        from_attributes = True
