import rasterio
import os

# Configure rasterio to use unsigned requests for public AWS S3 bucket
os.environ["AWS_NO_SIGN_REQUEST"] = "YES"

# Copernicus DEM 30m path for N18 E073
# The tile naming convention usually is Copernicus_DSM_COG_10_N18_00_E073_00_DEM
url = "s3://copernicus-dem-30m/Copernicus_DSM_COG_10_N18_00_E073_00_DEM/Copernicus_DSM_COG_10_N18_00_E073_00_DEM.tif"

print(f"Testing access to {url}")
try:
    with rasterio.open(url) as src:
        print(f"Success! Opened DEM.")
        print(f"CRS: {src.crs}")
        print(f"Bounds: {src.bounds}")
        print(f"Shape: {src.shape}")
        
        # Test sampling at Sinhagad fort (18.3663, 73.7558)
        coord = [(73.7558, 18.3663)]  # (lon, lat)
        elevation = list(src.sample(coord))[0][0]
        print(f"Elevation at Sinhagad: {elevation} meters")
except Exception as e:
    print(f"Error accessing DEM: {e}")
