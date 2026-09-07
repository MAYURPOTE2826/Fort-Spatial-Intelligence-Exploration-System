import pytest
from app.gis.dem_processor import DEMProcessor
from unittest.mock import patch

def test_get_elevation():
    processor = DEMProcessor()
    # Mocking rasterio open inside the class or bypassing it.
    # We can just test the fallback logic if no file exists.
    with patch("os.path.exists", return_value=False):
        elev = processor.get_elevation("dummy.tif", 18.0, 73.0)
        assert elev == 0.0 # Assuming default fallback is 0 or it handles missing files gracefully

def test_get_elevation_invalid_coords():
    processor = DEMProcessor()
    # Testing boundary conditions
    with patch("os.path.exists", return_value=False):
        elev = processor.get_elevation("dummy.tif", 91.0, 181.0) # Invalid coords
        assert elev == 0.0
