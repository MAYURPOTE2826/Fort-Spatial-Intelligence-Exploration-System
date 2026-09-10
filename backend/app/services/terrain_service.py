"""
TerrainService — elevation lookup using registered DEM tiles.

Uses DEMProcessor for bilinear interpolation from GeoTIFF files.
Elevation results are cached in-memory (module-level dict) keyed by rounded coordinates.
"""
import logging
from typing import Dict, Any, Optional, List, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.terrain import TerrainTile
from app.gis.dem_processor import dem_processor

logger = logging.getLogger(__name__)

# Simple in-memory cache: (rounded_lat, rounded_lon) → elevation result dict
_elevation_cache: Dict[Tuple[float, float], Dict[str, Any]] = {}

# Cache is rounded to 4 decimal places (~10m precision at equator)
_CACHE_PRECISION = 4


def _round_coord(v: float) -> float:
    return round(v, _CACHE_PRECISION)


class TerrainService:

    @staticmethod
    def get_elevation(db: Session, lat: float, lon: float) -> Dict[str, Any]:
        """
        Query the elevation for a specific point.

        Returns a dict:
          {
              "elevation_m": float | None,
              "accuracy_m": float | None,
              "source": str,
              "confidence": "high" | "medium" | "low" | "none"
          }
        """
        cache_key = (_round_coord(lat), _round_coord(lon))
        if cache_key in _elevation_cache:
            return _elevation_cache[cache_key]

        # Find which DEM tile covers this point using PostGIS ST_Contains
        try:
            point_geom = func.ST_SetSRID(func.ST_MakePoint(lon, lat), 4326)
            tile: Optional[TerrainTile] = (
                db.query(TerrainTile)
                .filter(func.ST_Contains(TerrainTile.geometry, point_geom))
                .first()
            )
        except Exception as e:
            logger.error(f"Error querying terrain tiles for ({lat}, {lon}): {e}")
            tile = None

        if not tile:
            logger.debug(f"No DEM tile found for coordinates: ({lat}, {lon})")
            result = {
                "elevation_m": None,
                "accuracy_m": None,
                "source": "unknown",
                "confidence": "none",
            }
            _elevation_cache[cache_key] = result
            return result

        # Query the DEM processor
        try:
            elevation = dem_processor.get_elevation(tile.file_path, lat, lon)
        except FileNotFoundError:
            logger.warning(f"DEM tile file not found: {tile.file_path}")
            elevation = None
        except Exception as e:
            logger.error(f"Error processing DEM tile '{tile.file_path}': {e}")
            elevation = None

        if elevation is None:
            result = {
                "elevation_m": None,
                "accuracy_m": getattr(tile, "resolution_m", None),
                "source": getattr(tile, "source", "unknown") or "unknown",
                "confidence": "low (nodata or out of bounds)",
            }
            _elevation_cache[cache_key] = result
            return result

        accuracy = getattr(tile, "resolution_m", None)
        if accuracy is not None and accuracy <= 30:
            confidence = "high"
        elif accuracy is not None and accuracy <= 90:
            confidence = "medium"
        else:
            confidence = "low"

        result = {
            "elevation_m": round(elevation, 2),
            "accuracy_m": accuracy,
            "source": getattr(tile, "source", "unknown") or "unknown",
            "confidence": confidence,
        }
        _elevation_cache[cache_key] = result
        return result

    @staticmethod
    def get_elevation_profile(
        db: Session,
        observer_lat: float,
        observer_lon: float,
        target_lat: float,
        target_lon: float,
        num_points: int = 100,
    ) -> List[Dict[str, Any]]:
        """
        Return an elevation profile between two points.

        Returns a list of dicts:
          [{"distance_km": float, "elevation_m": float | None, "lat": float, "lon": float}, ...]

        Used for terrain profile visualization.
        """
        from app.gis.visibility_engine import (
            haversine_distance,
            interpolate_points,
        )

        total_distance_m = haversine_distance(
            observer_lat, observer_lon, target_lat, target_lon
        )
        sample_points = interpolate_points(
            observer_lat, observer_lon, target_lat, target_lon, num_points
        )

        profile = []
        for i, (lat, lon) in enumerate(sample_points):
            dist_m = haversine_distance(observer_lat, observer_lon, lat, lon)
            elev_result = TerrainService.get_elevation(db, lat, lon)
            profile.append({
                "distance_km": round(dist_m / 1000.0, 3),
                "elevation_m": elev_result.get("elevation_m"),
                "lat": lat,
                "lon": lon,
                "index": i,
            })

        return profile

    @staticmethod
    def clear_cache() -> None:
        """Clear the in-memory elevation cache."""
        _elevation_cache.clear()


terrain_service = TerrainService()
