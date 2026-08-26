import math
from dataclasses import dataclass
from typing import Optional, List, Tuple
from .dem_processor import DEMProcessor

@dataclass
class VisibilityResult:
    fort_id: str
    distance_km: float
    bearing_deg: float
    direction: str
    observer_elevation: float
    target_elevation: float
    max_terrain_intersection: float
    visibility_status: str
    visibility_score: float
    obstruction_distance_km: Optional[float]
    confidence: float
    explanation: str

# Constants for Line-of-Sight calculation
EARTH_RADIUS_M = 6371000
REFRACTION_COEFFICIENT = 0.13
EFFECTIVE_EARTH_RADIUS_M = EARTH_RADIUS_M / (1 - REFRACTION_COEFFICIENT)

def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate the great circle distance in meters between two points."""
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    
    a = math.sin(delta_phi / 2.0) ** 2 + \
        math.cos(phi1) * math.cos(phi2) * \
        math.sin(delta_lambda / 2.0) ** 2
    
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return EARTH_RADIUS_M * c

def calculate_bearing(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate the initial bearing from point 1 to point 2 in degrees."""
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlon = lon2 - lon1
    
    x = math.sin(dlon) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1) * math.cos(lat2) * math.cos(dlon))
    
    initial_bearing = math.atan2(x, y)
    return (math.degrees(initial_bearing) + 360) % 360

def interpolate_points(lat1: float, lon1: float, lat2: float, lon2: float, num_points: int) -> List[Tuple[float, float]]:
    """Generate linearly interpolated points between two coordinates."""
    points = []
    for i in range(num_points):
        fraction = i / max(num_points - 1, 1)
        lat = lat1 + (lat2 - lat1) * fraction
        lon = lon1 + (lon2 - lon1) * fraction
        points.append((lat, lon))
    return points

def adjust_elevation_for_curvature(elevation: float, distance_from_start: float) -> float:
    """Adjust elevation to account for earth's curvature and atmospheric refraction."""
    drop = (distance_from_start ** 2) / (2 * EFFECTIVE_EARTH_RADIUS_M)
    return elevation - drop

def calculate_line_of_sight(
    observer_lat: float, 
    observer_lon: float, 
    observer_elevation: float, 
    observer_height: float,
    target_lat: float, 
    target_lon: float, 
    target_elevation: float, 
    target_height: float,
    dem_service: DEMProcessor,
    dem_file_path: str = "s3://copernicus-dem-30m/Copernicus_DSM_COG_10_N18_00_E073_00_DEM/Copernicus_DSM_COG_10_N18_00_E073_00_DEM.tif",
    target_id: str = "target"
) -> VisibilityResult:
    """
    Determines if a target is visible from an observer's location considering terrain.
    """
    total_distance_m = haversine_distance(observer_lat, observer_lon, target_lat, target_lon)
    total_distance_km = total_distance_m / 1000.0
    bearing = calculate_bearing(observer_lat, observer_lon, target_lat, target_lon)
    
    # from direction_engine import get_cardinal_direction (will be added after direction_engine is created)
    from .direction_engine import get_cardinal_direction
    direction = get_cardinal_direction(bearing)
    
    obs_total_z = observer_elevation + observer_height
    tgt_total_z = target_elevation + target_height
    
    # Adjust target elevation relative to observer due to earth curvature
    adj_tgt_z = adjust_elevation_for_curvature(tgt_total_z, total_distance_m)
    
    # Calculate initial viewing angle (slope) to the target
    dz_target = adj_tgt_z - obs_total_z
    target_slope = dz_target / total_distance_m if total_distance_m > 0 else 0
    
    # Sample points (adaptive, every ~100m)
    num_points = max(10, int(total_distance_m / 100))
    sample_points = interpolate_points(observer_lat, observer_lon, target_lat, target_lon, num_points)
    
    max_obstruction_elev = -float('inf')
    is_blocked = False
    obstruction_distance = None
    min_clearance = float('inf')
    
    # Skip the very first point (observer) and very last point (target) for obstruction checks
    for i in range(1, num_points - 1):
        pt_lat, pt_lon = sample_points[i]
        dist_i = haversine_distance(observer_lat, observer_lon, pt_lat, pt_lon)
        
        # Interpolate terrain elevation
        terrain_elev = dem_service.get_elevation(dem_file_path, pt_lat, pt_lon)
        
        if terrain_elev is None:
            # Fallback if outside DEM or nodata
            continue
            
        adj_terrain_elev = adjust_elevation_for_curvature(terrain_elev, dist_i)
        
        # Expected line-of-sight elevation at distance dist_i
        expected_los_elev = obs_total_z + (target_slope * dist_i)
        
        clearance = expected_los_elev - adj_terrain_elev
        min_clearance = min(min_clearance, clearance)
        
        if adj_terrain_elev > max_obstruction_elev:
            max_obstruction_elev = adj_terrain_elev
            
        if clearance < 0 and not is_blocked:
            is_blocked = True
            obstruction_distance = dist_i / 1000.0
            
    # Score Calculation
    # Factor 1: Terrain clearance
    # If clearance < 0, score drops heavily. If positive, caps at 1.0.
    if is_blocked:
        clearance_score = 0.0
    else:
        # Logistic curve based on min_clearance: 5m clearance -> 0.5, 20m -> 0.9
        clearance_score = 1 / (1 + math.exp(-0.2 * (min_clearance - 5)))
        
    # Factor 2: Distance penalty (farther = lower confidence/score)
    # Allows up to ~35km to remain >= 0.9 if clearance is perfect
    distance_score = math.exp(-0.003 * total_distance_km)
    
    # Factor 3: Observer height (higher gives a slight bump, up to +0.1)
    height_bonus = min(0.1, observer_height / 100.0)
    
    base_score = clearance_score * distance_score + height_bonus
    final_score = max(0.0, min(1.0, base_score))
    
    # If completely blocked by terrain, cap score at max 0.4
    if is_blocked:
        final_score = min(final_score, 0.4)
        
    if final_score >= 0.9:
        status = "VISIBLE"
        explanation = "Clear line of sight with good clearance and distance."
    elif final_score >= 0.5:
        status = "UNCERTAIN"
        explanation = "Line of sight is possible but clearance is low or distance is far."
    else:
        status = "BLOCKED"
        explanation = f"Line of sight blocked by terrain at {obstruction_distance:.2f} km." if is_blocked else "Score too low due to extreme distance or poor clearance."
        
    # Confidence calculation: higher if we have a lot of clearance or very blocked. Lower if on the edge.
    confidence_dist = math.exp(-0.02 * total_distance_km) # Confidence drops with distance
    # if clearance is near 0, confidence is low
    confidence_clearance = min(1.0, abs(min_clearance) / 20.0) if min_clearance != float('inf') else 0.5
    confidence = max(0.1, min(1.0, (confidence_dist + confidence_clearance) / 2.0))
    
    return VisibilityResult(
        fort_id=target_id,
        distance_km=total_distance_km,
        bearing_deg=bearing,
        direction=direction,
        observer_elevation=obs_total_z,
        target_elevation=tgt_total_z,
        max_terrain_intersection=max_obstruction_elev if max_obstruction_elev != -float('inf') else 0.0,
        visibility_status=status,
        visibility_score=final_score,
        obstruction_distance_km=obstruction_distance,
        confidence=confidence,
        explanation=explanation
    )
