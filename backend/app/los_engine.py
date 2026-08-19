import rasterio
import math
import numpy as np

# Adjust based on the actual bounding box or use a dict mapping regions to S3 URLs
# For MVP, we use the hardcoded N18E073 tile which covers Pune area forts
DEM_URL = "s3://copernicus-dem-30m/Copernicus_DSM_COG_10_N18_00_E073_00_DEM/Copernicus_DSM_COG_10_N18_00_E073_00_DEM.tif"

def haversine(lat1, lon1, lat2, lon2):
    R = 6371000  # radius of Earth in meters
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    a = math.sin(delta_phi/2.0)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda/2.0)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c

def calculate_bearing(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlon = lon2 - lon1
    x = math.sin(dlon) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1) * math.cos(lat2) * math.cos(dlon))
    initial_bearing = math.atan2(x, y)
    initial_bearing = math.degrees(initial_bearing)
    return (initial_bearing + 360) % 360

def extract_elevation_profile(lat1, lon1, lat2, lon2, num_points=100):
    """
    Extracts an elevation profile between two points using Rasterio.
    """
    lats = np.linspace(lat1, lat2, num_points)
    lons = np.linspace(lon1, lon2, num_points)
    coords = list(zip(lons, lats))
    
    elevations = []
    with rasterio.open(DEM_URL) as src:
        # Sample elevations along the line
        for val in src.sample(coords):
            elevations.append(val[0])
            
    return lats, lons, elevations

def check_line_of_sight(user_lat, user_lon, user_elevation, fort_lat, fort_lon, fort_elevation):
    """
    Checks if fort is visible from user location.
    Accounts for Earth curvature and refraction.
    """
    distance = haversine(user_lat, user_lon, fort_lat, fort_lon)
    num_points = max(10, int(distance / 30))  # One point roughly every 30m
    
    lats, lons, elevations = extract_elevation_profile(user_lat, user_lon, fort_lat, fort_lon, num_points)
    
    # Earth radius and refraction coefficient
    R = 6371000
    k = 0.13 # Standard refraction coefficient
    Re = R / (1 - k)
    
    # Calculate initial viewing angle to the fort
    # Adjusted fort elevation relative to curvature
    adj_fort_elev = fort_elevation - (distance**2) / (2 * Re)
    dz_fort = adj_fort_elev - user_elevation
    max_angle = math.atan2(dz_fort, distance)
    
    # Check intermediate points
    for i in range(1, num_points - 1):
        dist_i = haversine(user_lat, user_lon, lats[i], lons[i])
        if dist_i == 0: continue
        
        # Adjust elevation for curvature and refraction
        h_i = elevations[i] - (dist_i**2) / (2 * Re)
        dz_i = h_i - user_elevation
        
        angle_i = math.atan2(dz_i, dist_i)
        
        if angle_i > max_angle:
            return False, dist_i, elevations[i]  # Occluded
            
    return True, distance, max_angle
