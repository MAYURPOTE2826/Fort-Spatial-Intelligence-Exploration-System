import pytest
from app.gis.visibility_engine import haversine_distance

def test_haversine_distance():
    # Pune to Mumbai roughly 120km
    lat1, lon1 = 18.5204, 73.8567
    lat2, lon2 = 19.0760, 72.8777
    dist = haversine_distance(lat1, lon1, lat2, lon2)
    assert 115000 < dist < 125000 # Roughly 118km

def test_haversine_distance_zero():
    # Distance to self should be 0
    lat1, lon1 = 18.5204, 73.8567
    dist = haversine_distance(lat1, lon1, lat1, lon1)
    assert dist == 0.0

def test_haversine_distance_negative_coordinates():
    # Test with negative coordinates
    lat1, lon1 = -18.5204, -73.8567
    lat2, lon2 = -19.0760, -72.8777
    dist = haversine_distance(lat1, lon1, lat2, lon2)
    assert 115000 < dist < 125000 # Distance should be same as positive
