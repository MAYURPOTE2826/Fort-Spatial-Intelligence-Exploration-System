from sqlalchemy.orm import Session
from sqlalchemy import text
from app import models

def get_forts_within_radius(db: Session, lat: float, lon: float, radius_km: float = 50.0):
    """
    Returns forts within the specified radius using PostGIS ST_DWithin.
    SRID 4326 is used for lat/lon. Casting to geography is important for accurate meter-based distance.
    """
    radius_meters = radius_km * 1000
    
    # We use PostGIS ST_DWithin with geography casting for meters
    query = text("""
        SELECT id, name, base_elevation, ST_X(location::geometry) as lon, ST_Y(location::geometry) as lat
        FROM forts
        WHERE ST_DWithin(
            location::geography, 
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
            "base_elevation": row.base_elevation,
            "lat": row.lat,
            "lon": row.lon
        })
    return forts
