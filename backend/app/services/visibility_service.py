import json
import time
import hashlib
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import concurrent.futures
from sqlalchemy.orm import Session

from app import crud
from app.models.visibility import VisibilityQueryCache
from app.schemas.visibility import (
    VisibilityResponse, ObserverInfo, FortVisibilityItem,
    VisibilityNetworkResponse, NetworkVisibilityEdge
)
from app.gis.visibility_engine import calculate_line_of_sight
from app.gis.dem_processor import dem_processor

class VisibilityService:
    @staticmethod
    def _generate_cache_key(prefix: str, **kwargs) -> str:
        """Generate a deterministic cache key from parameters."""
        # Sort kwargs for consistent key generation
        sorted_items = sorted(kwargs.items())
        # Round floats to prevent cache misses due to tiny precision differences
        str_items = []
        for k, v in sorted_items:
            if isinstance(v, float):
                # Round coordinates/values to reasonable precision (e.g. ~10m for lat/lon)
                str_items.append(f"{k}:{round(v, 4)}")
            else:
                str_items.append(f"{k}:{v}")
        
        raw_key = f"{prefix}_" + "_".join(str_items)
        return hashlib.md5(raw_key.encode()).hexdigest()

    @staticmethod
    def _get_from_cache(db: Session, cache_key: str) -> Optional[dict]:
        cache_entry = db.query(VisibilityQueryCache).filter(
            VisibilityQueryCache.cache_key == cache_key,
            VisibilityQueryCache.expires_at > datetime.utcnow()
        ).first()
        if cache_entry:
            return json.loads(cache_entry.response_payload)
        return None

    @staticmethod
    def _save_to_cache(db: Session, cache_key: str, payload: dict, ttl_hours: int = 24):
        expires_at = datetime.utcnow() + timedelta(hours=ttl_hours)
        
        # Upsert cache entry
        existing = db.query(VisibilityQueryCache).filter_by(cache_key=cache_key).first()
        if existing:
            existing.response_payload = json.dumps(payload)
            existing.expires_at = expires_at
        else:
            new_entry = VisibilityQueryCache(
                cache_key=cache_key,
                response_payload=json.dumps(payload),
                expires_at=expires_at
            )
            db.add(new_entry)
        db.commit()

    @classmethod
    def calculate_visibility_from_location(
        cls, db: Session, lat: float, lon: float, 
        heading: Optional[float], fov: Optional[float], 
        radius_km: float, elevation: Optional[float], 
        observer_height: float
    ) -> VisibilityResponse:
        start_time = time.time()
        
        # 1. Check cache
        cache_key = cls._generate_cache_key(
            "loc", lat=lat, lon=lon, heading=heading, fov=fov, 
            radius_km=radius_km, elevation=elevation, height=observer_height
        )
        cached_result = cls._get_from_cache(db, cache_key)
        if cached_result:
            cached_result['calculation_time_ms'] = int((time.time() - start_time) * 1000)
            return VisibilityResponse(**cached_result)

        # 2. Get observer elevation if missing
        obs_elevation = elevation
        if obs_elevation is None:
            # Get from DEM
            obs_elevation = dem_processor.get_elevation(
                "s3://copernicus-dem-30m/Copernicus_DSM_COG_10_N18_00_E073_00_DEM/Copernicus_DSM_COG_10_N18_00_E073_00_DEM.tif", 
                lat, lon
            ) or 0.0

        # 3. Find nearby forts via PostGIS
        nearby_forts = crud.get_forts_within_radius(db, lat, lon, radius_km)
        
        if not nearby_forts:
            return VisibilityResponse(
                observer=ObserverInfo(lat=lat, lon=lon, elevation=obs_elevation, heading=heading, fov=fov, radius_km=radius_km),
                visible_forts=[], uncertain_forts=[], blocked_forts=[], calculation_time_ms=int((time.time() - start_time) * 1000)
            )

        # 4. Filter by FOV if provided
        filtered_forts = []
        for fort in nearby_forts:
            if heading is not None and fov is not None:
                # Calculate bearing to fort to see if it's within FOV
                from app.gis.visibility_engine import calculate_bearing
                bearing = calculate_bearing(lat, lon, fort["lat"], fort["lon"])
                
                # Check if bearing is within heading +/- (fov/2)
                diff = (bearing - heading + 180) % 360 - 180
                if abs(diff) <= (fov / 2):
                    fort["relative_angle"] = diff
                    filtered_forts.append(fort)
            else:
                filtered_forts.append(fort)

        # 5. Run Visibility Calculations concurrently
        def calc_fort(fort):
            result = calculate_line_of_sight(
                observer_lat=lat, observer_lon=lon,
                observer_elevation=obs_elevation, observer_height=observer_height,
                target_lat=fort["lat"], target_lon=fort["lon"],
                target_elevation=fort["base_elevation"], target_height=10.0, # assumed target height
                dem_service=dem_processor,
                target_id=str(fort["id"])
            )
            return fort, result

        visible_forts = []
        uncertain_forts = []
        blocked_forts = []

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            future_to_fort = {executor.submit(calc_fort, f): f for f in filtered_forts}
            for future in concurrent.futures.as_completed(future_to_fort):
                fort, v_result = future.result()
                
                item = FortVisibilityItem(
                    id=str(fort["id"]),
                    name=fort["name"],
                    distance_km=v_result.distance_km,
                    bearing_deg=v_result.bearing_deg,
                    direction=v_result.direction,
                    relative_angle=fort.get("relative_angle"),
                    visibility_score=v_result.visibility_score,
                    visibility_status=v_result.visibility_status,
                    elevation=fort["base_elevation"],
                    elevation_difference=fort["base_elevation"] - obs_elevation,
                    obstruction_distance_km=v_result.obstruction_distance_km,
                    confidence=v_result.confidence,
                    explanation=v_result.explanation
                )
                
                if v_result.visibility_status == "VISIBLE":
                    visible_forts.append(item)
                elif v_result.visibility_status == "UNCERTAIN":
                    uncertain_forts.append(item)
                else:
                    blocked_forts.append(item)

        # Sort by distance
        visible_forts.sort(key=lambda x: x.distance_km)
        uncertain_forts.sort(key=lambda x: x.distance_km)
        blocked_forts.sort(key=lambda x: x.distance_km)

        calc_time = int((time.time() - start_time) * 1000)
        
        response = VisibilityResponse(
            observer=ObserverInfo(lat=lat, lon=lon, elevation=obs_elevation, heading=heading, fov=fov, radius_km=radius_km),
            visible_forts=visible_forts,
            uncertain_forts=uncertain_forts,
            blocked_forts=blocked_forts,
            calculation_time_ms=calc_time
        )
        
        # Save to cache without the calculation_time_ms so it can be dynamically injected next time
        cache_payload = response.model_dump(mode="json")
        cls._save_to_cache(db, cache_key, cache_payload)
        
        return response

    @classmethod
    def calculate_visibility_between_forts(cls, db: Session, source_id: str, target_id: str) -> dict:
        # Get forts
        source = crud.get_fort_by_id(db, source_id)
        target = crud.get_fort_by_id(db, target_id)
        
        if not source or not target:
            raise ValueError("Invalid fort IDs provided")
            
        res = cls.calculate_visibility_from_location(
            db=db,
            lat=source["lat"],
            lon=source["lon"],
            heading=None, fov=None,
            radius_km=200, # big enough to contain the target
            elevation=source["base_elevation"],
            observer_height=1.7
        )
        
        # Filter to only the target fort
        target_item = None
        for pool in [res.visible_forts, res.uncertain_forts, res.blocked_forts]:
            for item in pool:
                if str(item.id) == str(target_id):
                    target_item = item
                    break
            if target_item:
                break
                
        # construct a custom response just for this
        if not target_item:
            raise ValueError("Target fort too far or could not be processed")
            
        return {
            "source_fort": source_id,
            "target_fort": target_id,
            "result": target_item.model_dump(mode="json"),
            "calculation_time_ms": res.calculation_time_ms
        }

    @classmethod
    def build_visibility_network(cls, db: Session, fort_ids: List[str]) -> VisibilityNetworkResponse:
        start_time = time.time()
        forts = crud.get_forts_by_ids(db, fort_ids)
        fort_dict = {str(f["id"]): f for f in forts}
        
        edges = []
        # Calculate N x (N-1) pairs, or we can just do a triangular matrix (since visibility is roughly symmetric, but curvature/height differ, let's just do directional)
        
        def check_pair(s_id, t_id):
            s = fort_dict[s_id]
            t = fort_dict[t_id]
            res = calculate_line_of_sight(
                observer_lat=s["lat"], observer_lon=s["lon"],
                observer_elevation=s["base_elevation"], observer_height=10.0, # fort tower height
                target_lat=t["lat"], target_lon=t["lon"],
                target_elevation=t["base_elevation"], target_height=10.0,
                dem_service=dem_processor,
                target_id=str(t_id)
            )
            return s_id, t_id, res

        pairs_to_check = []
        for s_id in fort_dict:
            for t_id in fort_dict:
                if s_id != t_id:
                    pairs_to_check.append((s_id, t_id))

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(check_pair, s, t) for s, t in pairs_to_check]
            for future in concurrent.futures.as_completed(futures):
                s_id, t_id, v_result = future.result()
                edges.append(NetworkVisibilityEdge(
                    source_id=s_id,
                    target_id=t_id,
                    is_visible=v_result.visibility_status == "VISIBLE",
                    distance_km=v_result.distance_km,
                    visibility_score=v_result.visibility_score
                ))

        return VisibilityNetworkResponse(
            nodes=list(fort_dict.keys()),
            edges=edges,
            calculation_time_ms=int((time.time() - start_time) * 1000)
        )
