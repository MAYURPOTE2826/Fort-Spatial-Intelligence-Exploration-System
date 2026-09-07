import pytest
from app.gis.visibility_engine import calculate_bearing

def test_calculate_bearing():
    # Pune to Mumbai is roughly North West
    lat1, lon1 = 18.5204, 73.8567
    lat2, lon2 = 19.0760, 72.8777
    bearing = calculate_bearing(lat1, lon1, lat2, lon2)
    assert 300 < bearing < 330 # NW is 315

def test_calculate_bearing_north():
    lat1, lon1 = 0, 0
    lat2, lon2 = 10, 0
    bearing = calculate_bearing(lat1, lon1, lat2, lon2)
    assert bearing == 0.0

def test_calculate_bearing_east():
    lat1, lon1 = 0, 0
    lat2, lon2 = 0, 10
    bearing = calculate_bearing(lat1, lon1, lat2, lon2)
    assert bearing == 90.0

def test_calculate_bearing_south():
    lat1, lon1 = 10, 0
    lat2, lon2 = 0, 0
    bearing = calculate_bearing(lat1, lon1, lat2, lon2)
    assert bearing == 180.0

def test_calculate_bearing_west():
    lat1, lon1 = 0, 10
    lat2, lon2 = 0, 0
    bearing = calculate_bearing(lat1, lon1, lat2, lon2)
    assert bearing == 270.0
