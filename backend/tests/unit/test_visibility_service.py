import pytest
from unittest.mock import patch, MagicMock
from app.services.visibility_service import VisibilityService

@pytest.fixture
def visibility_service():
    return VisibilityService()

@patch('app.services.visibility_service.terrain_service.get_elevation')
@patch('app.services.visibility_service.fort_service.get_forts_in_radius')
def test_calculate_visibility(mock_get_forts, mock_get_elevation, visibility_service, db_session):
    # Setup mocks
    mock_fort1 = MagicMock()
    mock_fort1.id = 1
    mock_fort1.name = "Test Fort 1"
    mock_fort1.latitude = 18.01
    mock_fort1.longitude = 73.01
    mock_fort1.elevation_m = 1000
    
    mock_get_forts.return_value = [mock_fort1]
    
    # Mock elevation profile to be flat, meaning it should be visible
    # get_elevation returns list of dicts with 'elevation'
    mock_get_elevation.side_effect = lambda lat, lon: 500
    
    # Run calculation
    # Let's patch the engine internal LOS check to return true
    with patch('app.services.visibility_service.los_engine.calculate_los', return_value=(True, [])):
        results = visibility_service.calculate_visibility(db_session, 18.00, 73.00, radius_km=10.0)
        
    assert len(results) == 1
    assert results[0]["is_visible"] is True
    assert results[0]["fort_name"] == "Test Fort 1"
