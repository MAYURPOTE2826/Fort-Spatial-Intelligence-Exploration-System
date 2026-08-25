from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.terrain import TerrainTile
from app.gis.dem_processor import dem_processor
from typing import Dict, Any, Optional
from functools import lru_cache
import logging

logger = logging.getLogger(__name__)

class TerrainService:
    
    @staticmethod
    @lru_cache(maxsize=1000)
    def _get_elevation_from_cache(db: Session, lat: float, lon: float) -> Dict[str, Any]:
        """
        Query the elevation for a specific point.
        """
        cache_key = f"{lat},{lon}"
        if cache_key in elevation_cache:
            return elevation_cache[cache_key]

        # Query the database to find which DEM tile contains this point
        # ST_SetSRID(ST_MakePoint(lon, lat), 4326)
        point_geom = func.ST_SetSRID(func.ST_MakePoint(lon, lat), 4326)
        
        tile = db.query(TerrainTile).filter(
            func.ST_Contains(TerrainTile.geometry, point_geom)
        ).first()

        if not tile:
            logger.warning(f"No DEM tile found for coordinates: {lat}, {lon}")
            return {
                "elevation_m": None,
                "accuracy_m": None,
                "source": "unknown",
                "confidence": "none"
            }

        # Query the processor
        try:
            elevation = dem_processor.get_elevation(tile.file_path, lat, lon)
        except Exception as e:
            logger.error(f"Error processing DEM tile {tile.file_path}: {e}")
            elevation = None

        if elevation is None:
            return {
                "elevation_m": None,
                "accuracy_m": tile.resolution_m,
                "source": tile.source or "unknown",
                "confidence": "low (nodata or out of bounds)"
            }

        # Determine confidence based on resolution
        accuracy = tile.resolution_m
        if accuracy is not None and accuracy <= 30:
            confidence = "high"
        elif accuracy is not None and accuracy <= 90:
            confidence = "medium"
        else:
            confidence = "low"

        result = {
            "elevation_m": round(elevation, 2),
            "accuracy_m": accuracy,
            "source": tile.source or "unknown",
            "confidence": confidence
        }
        
        elevation_cache[cache_key] = result
        return result

    @staticmethod
    def get_elevation_profile():
        pass
