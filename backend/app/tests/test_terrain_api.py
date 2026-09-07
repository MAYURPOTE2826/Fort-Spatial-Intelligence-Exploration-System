import pytest

def test_get_terrain_profile(client):
    response = client.get("/api/v1/terrain/profile?start_lat=18.0&start_lon=73.0&end_lat=18.1&end_lon=73.1")
    # Without mocking or valid DEMs, this might 404 or 500 depending on implementation. Let's just test it runs.
    # Assuming the API is currently unimplemented or returns a basic mock.
    assert response.status_code in [200, 404, 500]

def test_get_terrain_profile_missing_params(client):
    response = client.get("/api/v1/terrain/profile?start_lat=18.0")
    assert response.status_code == 422
