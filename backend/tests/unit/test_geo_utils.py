import pytest
from app.utils.geo import calculate_distance, calculate_bearing, bearing_to_direction

def test_calculate_distance():
    # Test distance between two known points (Pune and Mumbai roughly)
    lat1, lon1 = 18.5204, 73.8567
    lat2, lon2 = 19.0760, 72.8777
    distance = calculate_distance(lat1, lon1, lat2, lon2)
    
    assert isinstance(distance, float)
    # Distance should be around 118-120 km
    assert 115 < distance < 125

def test_calculate_bearing():
    # Pune to Mumbai is roughly North-West
    lat1, lon1 = 18.5204, 73.8567
    lat2, lon2 = 19.0760, 72.8777
    bearing = calculate_bearing(lat1, lon1, lat2, lon2)
    
    assert isinstance(bearing, float)
    assert 0 <= bearing < 360
    assert 300 < bearing < 330 # North-West

def test_bearing_to_direction():
    assert bearing_to_direction(0) == "N"
    assert bearing_to_direction(45) == "NE"
    assert bearing_to_direction(90) == "E"
    assert bearing_to_direction(135) == "SE"
    assert bearing_to_direction(180) == "S"
    assert bearing_to_direction(225) == "SW"
    assert bearing_to_direction(270) == "W"
    assert bearing_to_direction(315) == "NW"
    assert bearing_to_direction(360) == "N"
