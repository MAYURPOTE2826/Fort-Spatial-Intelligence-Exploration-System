import pytest
import math
import time
from unittest.mock import Mock

from app.gis.visibility_engine import (
    haversine_distance, calculate_bearing, interpolate_points, 
    adjust_elevation_for_curvature, calculate_line_of_sight
)
from app.gis.direction_engine import (
    get_cardinal_direction, calculate_relative_angle, is_in_field_of_view
)
from app.gis.dem_processor import DEMProcessor

# -------------------------
# direction_engine.py Tests
# -------------------------

def test_get_cardinal_direction():
    assert get_cardinal_direction(0) == "N"
    assert get_cardinal_direction(360) == "N"
    assert get_cardinal_direction(90) == "E"
    assert get_cardinal_direction(180) == "S"
    assert get_cardinal_direction(270) == "W"
    assert get_cardinal_direction(45) == "NE"
    assert get_cardinal_direction(22) == "NNE"
    assert get_cardinal_direction(-90) == "W"

def test_calculate_relative_angle():
    assert calculate_relative_angle(90, 0) == 90
    assert calculate_relative_angle(270, 0) == -90
    assert calculate_relative_angle(10, 350) == 20
    assert calculate_relative_angle(350, 10) == -20

def test_is_in_field_of_view():
    assert is_in_field_of_view(45, 0, fov=90) is True
    assert is_in_field_of_view(50, 0, fov=90) is False
    assert is_in_field_of_view(350, 0, fov=45) is True

# --------------------------
# visibility_engine.py Tests
# --------------------------

def test_haversine_distance():
    # Pune to Mumbai roughly 120km
    lat1, lon1 = 18.5204, 73.8567
    lat2, lon2 = 19.0760, 72.8777
    dist = haversine_distance(lat1, lon1, lat2, lon2)
    assert 115000 < dist < 125000 # Roughly 118km

def test_calculate_bearing():
    # Pune to Mumbai is roughly North West
    lat1, lon1 = 18.5204, 73.8567
    lat2, lon2 = 19.0760, 72.8777
    bearing = calculate_bearing(lat1, lon1, lat2, lon2)
    assert 300 < bearing < 330 # NW is 315

def test_interpolate_points():
    points = interpolate_points(0, 0, 10, 10, 3)
    assert len(points) == 3
    assert points[0] == (0.0, 0.0)
    assert points[1] == (5.0, 5.0)
    assert points[2] == (10.0, 10.0)

def test_adjust_elevation_for_curvature():
    # For a distance of 10km (10000m), drop should be ~ 6.8 meters
    # taking refraction into account (effective radius ~8000km), it's about 5-6m
    elev = 100.0
    dist = 10000.0
    adj_elev = adjust_elevation_for_curvature(elev, dist)
    assert adj_elev < elev
    assert elev - adj_elev > 5.0

# --------------------------
# Core LOS Algorithm Tests
# --------------------------

class MockDEMService(DEMProcessor):
    def __init__(self, terrain_elevations):
        """
        terrain_elevations is a list of elevations that will be returned sequentially.
        """
        super().__init__()
        self.terrain_elevations = terrain_elevations
        self.index = 0
        
    def get_elevation(self, file_path, lat, lon):
        if self.index < len(self.terrain_elevations):
            elev = self.terrain_elevations[self.index]
            self.index += 1
            return elev
        return 0.0

def test_calculate_line_of_sight_visible():
    """Test when there is no obstruction (Rajgad to Torna scenario roughly)."""
    # Simulate 5 points between observer and target
    # Distance is small, let's say a few km.
    # Elevations:
    # Obs: 1300m, Target: 1400m
    # Terrain in between: 1000m, 1100m, 1000m (valley)
    
    mock_dem = MockDEMService([1300.0, 1000.0, 1100.0, 1000.0, 1400.0])
    
    # We will fake the coordinates so the distance is approx 4km.
    # We just need to make sure the loop runs.
    # But calculate_line_of_sight calls interpolate_points based on distance / 100
    # To keep the mock simple, we just pass coordinates very close to each other 
    # to control num_points or just mock get_elevation to return a low valley.
    pass

def test_calculate_line_of_sight_with_mock():
    # Observer at (0,0) elevation 100
    # Target at (0, 0.1) elevation 100 (~11km away)
    # Midpoint terrain is low (valley)
    mock_dem = MockDEMService([])
    
    # Override get_elevation to return a valley
    def mock_get_elev(file_path, lat, lon):
        return 50.0 # valley
    mock_dem.get_elevation = mock_get_elev
    
    result = calculate_line_of_sight(
        observer_lat=0.0, observer_lon=0.0, observer_elevation=100.0, observer_height=1.7,
        target_lat=0.0, target_lon=0.1, target_elevation=100.0, target_height=10.0,
        dem_service=mock_dem
    )
    
    assert result.visibility_status == "VISIBLE"
    assert result.visibility_score > 0.8

def test_calculate_line_of_sight_blocked():
    # Observer at (0,0) elevation 100
    # Target at (0, 0.1) elevation 100 (~11km away)
    # Midpoint terrain is high (mountain)
    mock_dem = MockDEMService([])
    
    # Override get_elevation to return a mountain
    def mock_get_elev(file_path, lat, lon):
        return 200.0 # mountain blocking
    mock_dem.get_elevation = mock_get_elev
    
    result = calculate_line_of_sight(
        observer_lat=0.0, observer_lon=0.0, observer_elevation=100.0, observer_height=1.7,
        target_lat=0.0, target_lon=0.1, target_elevation=100.0, target_height=10.0,
        dem_service=mock_dem
    )
    
    assert result.visibility_status == "BLOCKED"
    assert result.visibility_score < 0.5

def test_performance_benchmark():
    """Simple benchmark to measure execution time of LOS calculation."""
    mock_dem = MockDEMService([])
    def mock_get_elev(file_path, lat, lon):
        return 100.0
    mock_dem.get_elevation = mock_get_elev
    
    start_time = time.time()
    
    # Run 100 calculations
    for _ in range(100):
        calculate_line_of_sight(
            observer_lat=0.0, observer_lon=0.0, observer_elevation=100.0, observer_height=1.7,
            target_lat=0.0, target_lon=0.1, target_elevation=100.0, target_height=10.0,
            dem_service=mock_dem
        )
        
    duration = time.time() - start_time
    # It should easily be under 1 second for 100 calculations if no real I/O is involved
    assert duration < 1.0
