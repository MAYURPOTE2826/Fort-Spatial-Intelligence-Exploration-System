import pytest
import os
import numpy as np
from app.gis.dem_processor import DEMProcessor
from app.services.terrain_service import TerrainService
import rasterio
from rasterio.transform import from_origin

@pytest.fixture
def dummy_dem_file(tmp_path):
    """Create a dummy GeoTIFF file for testing."""
    file_path = tmp_path / "dummy_dem.tif"
    
    # 3x3 grid
    data = np.array([
        [100.0, 110.0, 120.0],
        [105.0, 115.0, 125.0],
        [110.0, 120.0, 130.0]
    ], dtype=np.float32)
    
    # Origin at (73.0, 18.0), pixel size is 0.01 degrees
    transform = from_origin(73.0, 18.0, 0.01, 0.01)
    
    with rasterio.open(
        file_path, 'w', driver='GTiff',
        height=data.shape[0], width=data.shape[1],
        count=1, dtype=data.dtype,
        crs='+proj=latlong',
        transform=transform,
        nodata=-9999.0
    ) as dst:
        dst.write(data, 1)
        
    return str(file_path)

def test_dem_processor_valid_point(dummy_dem_file):
    processor = DEMProcessor()
    
    # Exact center of top-left pixel (73.0 + 0.005, 18.0 - 0.005)
    # Rasterio from_origin defines top-left corner.
    # col 0, row 0 -> lon 73.0 to 73.01, lat 17.99 to 18.0
    # center is lon 73.005, lat 17.995
    lon, lat = 73.005, 17.995
    
    elevation = processor.get_elevation(dummy_dem_file, lat, lon)
    
    # It should be exactly 100.0 if we hit the pixel center and don't interpolate
    # With bilinear interpolation on the center, it's 100.0
    assert elevation is not None
    assert round(elevation, 2) == 100.0
    
    # Center of middle pixel
    lon, lat = 73.015, 17.985
    elevation = processor.get_elevation(dummy_dem_file, lat, lon)
    assert round(elevation, 2) == 115.0

def test_dem_processor_interpolation(dummy_dem_file):
    processor = DEMProcessor()
    
    # Halfway between (73.005, 17.995) which is 100.0 and (73.015, 17.995) which is 110.0
    lon, lat = 73.010, 17.995
    elevation = processor.get_elevation(dummy_dem_file, lat, lon)
    assert round(elevation, 2) == 105.0

def test_dem_processor_out_of_bounds(dummy_dem_file):
    processor = DEMProcessor()
    
    lon, lat = 74.0, 19.0
    elevation = processor.get_elevation(dummy_dem_file, lat, lon)
    assert elevation is None

def test_terrain_service_cache(mocker):
    # Mock the DB
    mock_db = mocker.Mock()
    
    # Create a mock TerrainTile
    mock_tile = mocker.Mock()
    mock_tile.file_path = "fake/path.tif"
    mock_tile.resolution_m = 30
    mock_tile.source = "copernicus"
    
    # Setup the query chain
    mock_query = mocker.Mock()
    mock_filter = mocker.Mock()
    mock_filter.first.return_value = mock_tile
    mock_query.filter.return_value = mock_filter
    mock_db.query.return_value = mock_query
    
    # Mock DEMProcessor
    mocker.patch('app.services.terrain_service.dem_processor.get_elevation', return_value=123.45)
    
    # Clear cache before testing
    TerrainService._get_elevation_from_cache.cache_clear()
    
    # Call once
    res1 = TerrainService._get_elevation_from_cache(mock_db, 18.0, 73.0)
    assert res1['elevation_m'] == 123.45
    assert mock_db.query.called
    
    # Reset mock to verify cache hit
    mock_db.query.reset_mock()
    
    # Call again
    res2 = TerrainService._get_elevation_from_cache(mock_db, 18.0, 73.0)
    assert res2['elevation_m'] == 123.45
    # Should not have queried DB again
    assert not mock_db.query.called
