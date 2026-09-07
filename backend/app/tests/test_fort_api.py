import pytest
from app.models.fort import Fort
from app.core.database import get_db

def test_get_forts(client, db_session):
    # Setup test data
    fort1 = Fort(id=1, name="Rajgad", latitude=18.0, longitude=73.0)
    fort2 = Fort(id=2, name="Torna", latitude=18.1, longitude=73.1)
    db_session.add_all([fort1, fort2])
    db_session.commit()
    
    response = client.get("/api/v1/forts/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["name"] == "Rajgad"

def test_get_fort_by_id(client, db_session):
    fort = Fort(id=1, name="Rajgad", latitude=18.0, longitude=73.0)
    db_session.add(fort)
    db_session.commit()
    
    response = client.get("/api/v1/forts/1")
    assert response.status_code == 200
    assert response.json()["name"] == "Rajgad"

def test_get_fort_not_found(client):
    response = client.get("/api/v1/forts/999")
    assert response.status_code == 404
