from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.visibility import VisibilityRequest, VisibleFortResponse
from app import crud
from app import los_engine
import math

router = APIRouter()

@router.post("/", response_model=List[VisibleFortResponse])
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
