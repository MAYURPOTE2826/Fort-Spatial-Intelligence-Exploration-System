from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.database import engine, Base
from app import models

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize the database tables if they don't exist
    # Note: In production, we should use Alembic for migrations
    Base.metadata.create_all(bind=engine)
    yield
    # Cleanup on shutdown

app = FastAPI(title="FortSight AI Backend", lifespan=lifespan)

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "FortSight AI Backend is running"}

from pydantic import BaseModel
from typing import List, Optional
from fastapi import Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app import crud
from app import los_engine
import math

class VisibilityRequest(BaseModel):
    lat: float
    lon: float
    elevation: Optional[float] = None
    radius_km: float = 50.0

class VisibleFortResponse(BaseModel):
    name: str
    lat: float
    lon: float
    distance_km: float
    bearing: float
    is_visible: bool
    elevation_angle: float
    
@app.post("/api/visibility", response_model=List[VisibleFortResponse])
def get_visible_forts(req: VisibilityRequest, db: Session = Depends(get_db)):
    # 1. Find nearby forts via PostGIS
    nearby_forts = crud.get_forts_within_radius(db, req.lat, req.lon, req.radius_km)
    
    results = []
    for fort in nearby_forts:
        # Snap user elevation to DEM if not provided
        if req.elevation is None:
            user_elev = los_engine.extract_elevation_profile(req.lat, req.lon, req.lat, req.lon, 1)[2][0] + 2.0
        else:
            user_elev = req.elevation
            
        # 2. Calculate LOS
        is_visible, distance, max_angle = los_engine.check_line_of_sight(
            user_lat=req.lat,
            user_lon=req.lon,
            user_elevation=user_elev,
            fort_lat=fort.lat,
            fort_lon=fort.lon,
            fort_elevation=fort["base_elevation"]
        )
        
        bearing = los_engine.calculate_bearing(req.lat, req.lon, fort.lat, fort.lon)
        
        results.append(VisibleFortResponse(
            name=fort["name"],
            lat=fort.lat,
            lon=fort.lon,
            distance_km=distance / 1000.0,
            bearing=bearing,
            is_visible=is_visible,
            elevation_angle=math.degrees(max_angle)
        ))
        
    return results

