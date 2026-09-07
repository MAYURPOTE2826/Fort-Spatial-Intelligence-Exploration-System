import pytest
from unittest.mock import patch

@patch("app.api.v1.endpoints.visibility.calculate_line_of_sight")
def test_calculate_visibility(mock_los, client):
    mock_los.return_value.visibility_status = "VISIBLE"
    mock_los.return_value.visibility_score = 1.0
    mock_los.return_value.distance = 1000.0
    
    payload = {
        "observer_lat": 18.0,
        "observer_lon": 73.0,
        "target_lat": 18.1,
        "target_lon": 73.1,
        "observer_height": 1.7,
        "target_height": 10.0
    }
    
    response = client.post("/api/v1/visibility/calculate", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data["visibility_status"] == "VISIBLE"

def test_calculate_visibility_invalid_input(client):
    payload = {
        "observer_lat": 200.0, # Invalid lat
        "observer_lon": 73.0,
        "target_lat": 18.1,
        "target_lon": 73.1
    }
    response = client.post("/api/v1/visibility/calculate", json=payload)
    assert response.status_code == 422
