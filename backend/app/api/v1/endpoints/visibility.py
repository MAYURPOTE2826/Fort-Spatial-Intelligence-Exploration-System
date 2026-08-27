from fastapi import APIRouter, Depends, Request, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.visibility import (
    VisibilityResponse, BetweenFortsRequest, BuildNetworkRequest, VisibilityNetworkResponse
)
from app.services.visibility_service import VisibilityService

from app.core.rate_limit import limiter

router = APIRouter()

@router.get("/from-location", response_model=VisibilityResponse)
@limiter.limit("10/minute")
def get_visibility_from_location(
    request: Request,
    lat: float = Query(..., ge=-90, le=90, description="Observer latitude"),
    lon: float = Query(..., ge=-180, le=180, description="Observer longitude"),
    heading: float = Query(None, ge=0, le=360, description="Compass heading (0-360)"),
    fov: float = Query(60, ge=1, le=180, description="Field of view in degrees"),
    radius_km: float = Query(50, ge=1, le=200, description="Search radius in km"),
    elevation: float = Query(None, description="Observer elevation above ground level in meters. Auto-calculated if missing."),
    observer_height: float = Query(1.7, description="Observer eye height above ground (meters)"),
    db: Session = Depends(get_db)
):
    return VisibilityService.calculate_visibility_from_location(
        db=db, lat=lat, lon=lon, heading=heading, fov=fov,
        radius_km=radius_km, elevation=elevation, observer_height=observer_height
    )

@router.post("/between-forts", response_model=dict)
@limiter.limit("20/minute")
def get_visibility_between_forts(
    request: Request,
    req: BetweenFortsRequest,
    db: Session = Depends(get_db)
):
    return VisibilityService.calculate_visibility_between_forts(
        db=db, source_id=req.source_fort_id, target_id=req.target_fort_id
    )

@router.post("/build-network", response_model=VisibilityNetworkResponse)
@limiter.limit("2/minute")
def build_visibility_network(
    request: Request,
    req: BuildNetworkRequest,
    db: Session = Depends(get_db)
):
    return VisibilityService.build_visibility_network(db=db, fort_ids=req.fort_ids)
