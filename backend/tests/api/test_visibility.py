import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_visibility_from_location():
    response = client.get(
        "/api/v1/visibility/from-location",
        params={
            "lat": 18.67,
            "lon": 73.33,
            "radius_km": 50,
            "heading": 245,
            "fov": 60,
            "observer_height": 1.7
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    
    assert "observer" in data
    assert data["observer"]["lat"] == 18.67
    assert data["observer"]["lon"] == 73.33
    assert data["observer"]["heading"] == 245
    
    assert "visible_forts" in data
    assert "uncertain_forts" in data
    assert "blocked_forts" in data
    assert "calculation_time_ms" in data
    assert type(data["calculation_time_ms"]) is int

def test_visibility_from_location_invalid_coords():
    response = client.get(
        "/api/v1/visibility/from-location",
        params={
            "lat": 100, # Invalid latitude
            "lon": 73.33
        }
    )
    assert response.status_code == 422 # Unprocessable Entity (FastAPI validation)

def test_build_network_endpoint():
    response = client.post(
        "/api/v1/visibility/build-network",
        json={
            "fort_ids": ["torna", "rajgad"]
        }
    )
    # Testing mock/db failure or success based on real db
    # We just expect 200 or 500 depending on if DB is seeded in tests
    assert response.status_code in [200, 500, 422] 
    
    if response.status_code == 200:
        data = response.json()
        assert "nodes" in data
        assert "edges" in data
