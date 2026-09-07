import pytest
from app.models.forts import Fort

def test_read_main(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "Welcome" in response.json()["message"]

def test_get_forts_empty(client):
    response = client.get("/api/v1/forts/")
    assert response.status_code == 200
    assert response.json() == []

def test_create_and_get_fort(client, db_session):
    # Seed db
    fort = Fort(name="Integration Fort", name_marathi="किल्ला", latitude=18.5, longitude=73.5, elevation_m=1200, type="Hill", difficulty="Medium")
    db_session.add(fort)
    db_session.commit()
    
    response = client.get("/api/v1/forts/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Integration Fort"

@pytest.mark.skip(reason="Requires mocked external terrain/visibility dependencies")
def test_visibility_endpoint(client):
    response = client.post("/api/v1/visibility/calculate", json={"latitude": 18.5, "longitude": 73.5, "radius_km": 50})
    assert response.status_code == 200
    assert "visible_forts" in response.json()
