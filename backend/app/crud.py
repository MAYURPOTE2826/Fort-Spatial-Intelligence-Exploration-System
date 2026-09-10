from sqlalchemy.orm import Session
from sqlalchemy import text
from app import models


def get_forts_within_radius(db: Session, lat: float, lon: float, radius_km: float = 50.0):
    """
    Returns forts within the specified radius using PostGIS ST_DWithin.
    Uses geography casting for accurate meter-based distance calculation.
    Column names match the 'forts' table: geometry (POINT), elevation (float).
    """
    radius_meters = radius_km * 1000

    query = text("""
        SELECT
            id,
            name,
            elevation AS base_elevation,
            ST_X(geometry::geometry) AS lon,
            ST_Y(geometry::geometry) AS lat
        FROM forts
        WHERE ST_DWithin(
            geometry::geography,
            ST_SetSRID(ST_MakePoint(:lon, :lat), 4326)::geography,
            :radius_meters
        )
    """)

    result = db.execute(query, {"lon": lon, "lat": lat, "radius_meters": radius_meters})

    forts = []
    for row in result:
        forts.append({
            "id": row.id,
            "name": row.name,
            "base_elevation": row.base_elevation or 0.0,
            "lat": row.lat,
            "lon": row.lon,
        })
    return forts


def get_fort_by_id(db: Session, fort_id: str):
    """
    Fetch a single fort by ID. Returns dict with geometry extracted as lat/lon.
    """
    query = text("""
        SELECT
            id,
            name,
            elevation AS base_elevation,
            ST_X(geometry::geometry) AS lon,
            ST_Y(geometry::geometry) AS lat
        FROM forts
        WHERE id = :id
    """)
    result = db.execute(query, {"id": fort_id}).fetchone()
    if result:
        return {
            "id": result.id,
            "name": result.name,
            "base_elevation": result.base_elevation or 0.0,
            "lat": result.lat,
            "lon": result.lon,
        }
    return None


def get_forts_by_ids(db: Session, fort_ids: list[str]):
    """
    Fetch multiple forts by a list of IDs.
    """
    query = text("""
        SELECT
            id,
            name,
            elevation AS base_elevation,
            ST_X(geometry::geometry) AS lon,
            ST_Y(geometry::geometry) AS lat
        FROM forts
        WHERE id = ANY(:ids)
    """)
    result = db.execute(query, {"ids": [int(i) for i in fort_ids]})
    forts = []
    for row in result:
        forts.append({
            "id": row.id,
            "name": row.name,
            "base_elevation": row.base_elevation or 0.0,
            "lat": row.lat,
            "lon": row.lon,
        })
    return forts
