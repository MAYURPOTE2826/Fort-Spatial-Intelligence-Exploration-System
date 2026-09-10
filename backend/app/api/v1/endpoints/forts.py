"""
Forts API endpoints — real database-backed implementation.

All data is served from the PostgreSQL/PostGIS database.
Mock data has been removed. Use `scripts/seed_forts.py` to load initial data.
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import text, or_, func
from typing import Any, Optional, List
from app.core.database import get_db
from app.models.forts import Fort, FortViewpoint, FortStructure, FortTrail, FortConnection

router = APIRouter()


def _fort_to_dict(fort: Fort) -> dict:
    """Serialize a Fort ORM object to a response dict, extracting geometry as lat/lon."""
    # Extract lat/lon from PostGIS geometry via SQL scalar
    return {
        "id": fort.id,
        "name": fort.name,
        "marathi_name": fort.marathi_name,
        "description": fort.description,
        "elevation": fort.elevation,
        "district": fort.district,
        "difficulty": fort.difficulty,
        "best_season": fort.best_season,
        "history": fort.history,
        "image_url": fort.image_url,
        "source": fort.source,
        # geometry will be resolved by caller using raw SQL
    }


@router.get("/")
def get_forts(
    db: Session = Depends(get_db),
    search: Optional[str] = Query(None, description="Search by name or Marathi name"),
    district: Optional[str] = Query(None, description="Filter by district"),
    difficulty: Optional[str] = Query(None, description="Filter by difficulty"),
    min_elevation: Optional[float] = Query(None, description="Minimum elevation in meters"),
    max_elevation: Optional[float] = Query(None, description="Maximum elevation in meters"),
    sort_by: str = Query("name", description="Sort field: name | elevation | difficulty"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(50, ge=1, le=200, description="Items per page"),
) -> Any:
    """Retrieve forts list with optional search, filtering and sorting."""
    query_sql = """
        SELECT
            id, name, marathi_name, description, elevation,
            district, difficulty, best_season, history, image_url, source,
            ST_Y(geometry::geometry) AS latitude,
            ST_X(geometry::geometry) AS longitude
        FROM forts
        WHERE 1=1
    """
    params: dict = {}

    if search:
        query_sql += " AND (name ILIKE :search OR marathi_name ILIKE :search)"
        params["search"] = f"%{search}%"
    if district:
        query_sql += " AND district ILIKE :district"
        params["district"] = f"%{district}%"
    if difficulty:
        query_sql += " AND difficulty ILIKE :difficulty"
        params["difficulty"] = f"%{difficulty}%"
    if min_elevation is not None:
        query_sql += " AND elevation >= :min_elev"
        params["min_elev"] = min_elevation
    if max_elevation is not None:
        query_sql += " AND elevation <= :max_elev"
        params["max_elev"] = max_elevation

    # Sorting — whitelist to prevent SQL injection
    sort_map = {"name": "name", "elevation": "elevation DESC NULLS LAST", "difficulty": "difficulty"}
    order_clause = sort_map.get(sort_by, "name")
    query_sql += f" ORDER BY {order_clause}"

    # Count total for pagination
    count_sql = f"SELECT COUNT(*) FROM ({query_sql}) AS sub"
    total = db.execute(text(count_sql), params).scalar() or 0

    # Apply pagination
    offset = (page - 1) * page_size
    query_sql += " LIMIT :limit OFFSET :offset"
    params["limit"] = page_size
    params["offset"] = offset

    rows = db.execute(text(query_sql), params).fetchall()

    forts_list = []
    for row in rows:
        forts_list.append({
            "id": row.id,
            "name": row.name,
            "marathi_name": row.marathi_name,
            "description": row.description,
            "elevation": row.elevation,
            "district": row.district,
            "difficulty": row.difficulty,
            "best_season": row.best_season,
            "history": row.history,
            "image_url": row.image_url,
            "source": row.source,
            "latitude": row.latitude,
            "longitude": row.longitude,
        })

    return {
        "items": forts_list,
        "total": total,
        "page": page,
        "page_size": page_size,
        "pages": max(1, -(-total // page_size)),  # ceiling division
    }


@router.get("/{fort_id}")
def get_fort(fort_id: int, db: Session = Depends(get_db)) -> Any:
    """Get fort details by ID."""
    row = db.execute(text("""
        SELECT
            id, name, marathi_name, description, elevation,
            district, difficulty, best_season, history, image_url, source,
            ST_Y(geometry::geometry) AS latitude,
            ST_X(geometry::geometry) AS longitude
        FROM forts
        WHERE id = :id
    """), {"id": fort_id}).fetchone()

    if not row:
        raise HTTPException(status_code=404, detail=f"Fort with id={fort_id} not found")

    return {
        "id": row.id,
        "name": row.name,
        "marathi_name": row.marathi_name,
        "description": row.description,
        "elevation": row.elevation,
        "district": row.district,
        "difficulty": row.difficulty,
        "best_season": row.best_season,
        "history": row.history,
        "image_url": row.image_url,
        "source": row.source,
        "latitude": row.latitude,
        "longitude": row.longitude,
    }


@router.get("/{fort_id}/structures")
def get_fort_structures(fort_id: int, db: Session = Depends(get_db)) -> Any:
    """Get internal structures of a fort."""
    # Verify fort exists
    fort = db.query(Fort).filter(Fort.id == fort_id).first()
    if not fort:
        raise HTTPException(status_code=404, detail=f"Fort with id={fort_id} not found")

    rows = db.execute(text("""
        SELECT
            id, fort_id, name, type, description,
            ST_Y(geometry::geometry) AS latitude,
            ST_X(geometry::geometry) AS longitude
        FROM fort_structures
        WHERE fort_id = :fort_id
        ORDER BY name
    """), {"fort_id": fort_id}).fetchall()

    items = []
    for row in rows:
        items.append({
            "id": row.id,
            "fort_id": row.fort_id,
            "name": row.name,
            "type": row.type,
            "description": row.description,
            "latitude": row.latitude,
            "longitude": row.longitude,
        })
    return {"items": items, "total": len(items)}


@router.get("/{fort_id}/viewpoints")
def get_fort_viewpoints(fort_id: int, db: Session = Depends(get_db)) -> Any:
    """Get viewpoints of a fort."""
    fort = db.query(Fort).filter(Fort.id == fort_id).first()
    if not fort:
        raise HTTPException(status_code=404, detail=f"Fort with id={fort_id} not found")

    rows = db.execute(text("""
        SELECT
            id, fort_id, name, type, elevation, description,
            ST_Y(geometry::geometry) AS latitude,
            ST_X(geometry::geometry) AS longitude
        FROM fort_viewpoints
        WHERE fort_id = :fort_id
        ORDER BY name
    """), {"fort_id": fort_id}).fetchall()

    items = []
    for row in rows:
        items.append({
            "id": row.id,
            "fort_id": row.fort_id,
            "name": row.name,
            "type": row.type,
            "elevation": row.elevation,
            "description": row.description,
            "latitude": row.latitude,
            "longitude": row.longitude,
        })
    return {"items": items, "total": len(items)}


@router.get("/{fort_id}/trails")
def get_fort_trails(fort_id: int, db: Session = Depends(get_db)) -> Any:
    """Get trails for a fort."""
    fort = db.query(Fort).filter(Fort.id == fort_id).first()
    if not fort:
        raise HTTPException(status_code=404, detail=f"Fort with id={fort_id} not found")

    rows = db.execute(text("""
        SELECT
            id, fort_id, name, difficulty,
            distance_km, estimated_time_hours,
            ST_AsGeoJSON(geometry) AS geometry_geojson
        FROM fort_trails
        WHERE fort_id = :fort_id
        ORDER BY name
    """), {"fort_id": fort_id}).fetchall()

    items = []
    for row in rows:
        items.append({
            "id": row.id,
            "fort_id": row.fort_id,
            "name": row.name,
            "difficulty": row.difficulty,
            "distance_km": row.distance_km,
            "estimated_time_hours": row.estimated_time_hours,
            "geometry": row.geometry_geojson,  # GeoJSON LineString string
        })
    return {"items": items, "total": len(items)}


@router.get("/{fort_id}/connections")
def get_fort_connections(fort_id: int, db: Session = Depends(get_db)) -> Any:
    """Get pre-calculated visibility connections for a fort."""
    fort = db.query(Fort).filter(Fort.id == fort_id).first()
    if not fort:
        raise HTTPException(status_code=404, detail=f"Fort with id={fort_id} not found")

    rows = db.execute(text("""
        SELECT
            fc.source_fort_id,
            fc.target_fort_id,
            f.name AS target_fort_name,
            f.marathi_name AS target_fort_marathi_name,
            fc.distance_km,
            fc.bearing_deg,
            fc.visibility_status,
            fc.visibility_score,
            fc.last_calculated_at
        FROM fort_connections fc
        JOIN forts f ON f.id = fc.target_fort_id
        WHERE fc.source_fort_id = :fort_id
        ORDER BY fc.distance_km
    """), {"fort_id": fort_id}).fetchall()

    items = []
    for row in rows:
        items.append({
            "source_fort_id": row.source_fort_id,
            "target_fort_id": row.target_fort_id,
            "target_fort_name": row.target_fort_name,
            "target_fort_marathi_name": row.target_fort_marathi_name,
            "distance_km": row.distance_km,
            "bearing_deg": row.bearing_deg,
            "visibility_status": row.visibility_status,
            "visibility_score": row.visibility_score,
            "last_calculated_at": row.last_calculated_at.isoformat() if row.last_calculated_at else None,
        })
    return {"items": items, "total": len(items)}
