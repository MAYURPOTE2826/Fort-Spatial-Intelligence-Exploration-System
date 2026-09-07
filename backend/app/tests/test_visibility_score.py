import pytest
from app.gis.visibility_engine import calculate_line_of_sight
from app.gis.dem_processor import DEMProcessor

class MockDEMService(DEMProcessor):
    def __init__(self, terrain_elevations):
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
    mock_dem = MockDEMService([])
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
    mock_dem = MockDEMService([])
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
