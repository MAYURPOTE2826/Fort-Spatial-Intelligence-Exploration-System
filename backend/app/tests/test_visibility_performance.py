import pytest
import time
from app.gis.visibility_engine import calculate_line_of_sight
from app.tests.test_visibility_score import MockDEMService

def test_performance_visibility_calculation():
    mock_dem = MockDEMService([])
    def mock_get_elev(file_path, lat, lon):
        return 100.0
    mock_dem.get_elevation = mock_get_elev
    
    start_time = time.time()
    
    for _ in range(100):
        calculate_line_of_sight(
            observer_lat=0.0, observer_lon=0.0, observer_elevation=100.0, observer_height=1.7,
            target_lat=0.0, target_lon=0.1, target_elevation=100.0, target_height=10.0,
            dem_service=mock_dem
        )
        
    duration = time.time() - start_time
    assert duration < 1.0 # 100 calculations should be under 1 sec
