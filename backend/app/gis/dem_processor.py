import os
import rasterio
from rasterio.windows import Window
import numpy as np
from typing import Optional, Tuple
from functools import lru_cache

class DEMProcessor:
    """Processor for Digital Elevation Model (DEM) files."""
    
    def __init__(self, cache_size: int = 5):
        self.cache_size = cache_size

    @lru_cache(maxsize=5)
    def _get_dataset(self, file_path: str):
        """Open and cache the rasterio dataset."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"DEM file not found: {file_path}")
        return rasterio.open(file_path)
    
    def get_elevation(self, file_path: str, lat: float, lon: float) -> Optional[float]:
        """
        Get the elevation at the given latitude and longitude using bilinear interpolation.
        Returns None if the point is outside the DEM bounds or falls on a NoData value.
        """
        dataset = self._get_dataset(file_path)
        
        # Check if point is within bounds
        if not (dataset.bounds.left <= lon <= dataset.bounds.right and 
                dataset.bounds.bottom <= lat <= dataset.bounds.top):
            return None
            
        # Get the row and column in the raster grid
        row, col = dataset.index(lon, lat)
        
        # We need the 2x2 grid around the point for bilinear interpolation
        # rasterio's index() returns the nearest integer pixel index
        # To do accurate bilinear interpolation, we need the exact continuous pixel coordinates
        # ~transform is the inverse transform (from spatial to pixel)
        col_float, row_float = ~dataset.transform * (lon, lat)
        
        # Find the top-left pixel of the 2x2 grid
        col_idx = int(np.floor(col_float - 0.5))
        row_idx = int(np.floor(row_float - 0.5))
        
        # Read the 2x2 window
        # Add 1 to width and height to cover the 4 points, but since col_idx/row_idx might be negative or at the edge,
        # we clamp or pad it. For simplicity in edge cases, we'll just read a 2x2 window.
        try:
            window = Window(col_idx, row_idx, 2, 2)
            data = dataset.read(1, window=window)
        except Exception:
            # Fallback for edge cases
            data = None
            
        if data is None or data.shape != (2, 2):
            # Fallback to nearest neighbor if at the very edge of the raster
            try:
                val = dataset.read(1, window=Window(col, row, 1, 1))[0, 0]
                return self._handle_nodata(val, dataset.nodata)
            except Exception:
                return None
                
        # Handle nodata in the 2x2 grid
        nodata = dataset.nodata
        if nodata is not None:
            if np.any(data == nodata) or np.any(np.isnan(data)):
                # If any of the 4 points is nodata, fallback to nearest neighbor to avoid complex interpolation
                # or return the valid nearest point. Here we just return nearest neighbor
                val = dataset.read(1, window=Window(col, row, 1, 1))[0, 0]
                return self._handle_nodata(val, nodata)

        # Bilinear interpolation
        # The fractional part of the coordinates
        u = col_float - 0.5 - col_idx
        v = row_float - 0.5 - row_idx
        
        # Interpolate along the top and bottom rows
        top = data[0, 0] * (1 - u) + data[0, 1] * u
        bottom = data[1, 0] * (1 - u) + data[1, 1] * u
        
        # Interpolate vertically
        elevation = top * (1 - v) + bottom * v
        
        return float(elevation)
        
    def _handle_nodata(self, val: float, nodata: Optional[float]) -> Optional[float]:
        """Return None if value is nodata."""
        if nodata is not None and val == nodata:
            return None
        if np.isnan(val):
            return None
        return float(val)

    def close(self):
        """Close all cached datasets."""
        self._get_dataset.cache_clear()

# Global instance for use across the application
dem_processor = DEMProcessor()
