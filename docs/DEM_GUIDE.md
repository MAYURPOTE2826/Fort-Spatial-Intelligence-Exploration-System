# FortSight AI: DEM (Digital Elevation Model) Guide

This guide explains how to acquire and process Digital Elevation Model (DEM) data for FortSight AI's terrain engine. The terrain engine requires this data to compute elevation for any given point (latitude, longitude) and to perform Line-of-Sight (LoS) calculations.

## Supported DEM Sources

We currently support any DEM data in **GeoTIFF** format, but we recommend:

1. **Copernicus DEM (GLO-30)**
   - **Resolution:** 30 meters
   - **Coverage:** Global
   - **Cost:** Free
   - **Best for:** Most accurate global terrain data currently available for free.

2. **NASA SRTM**
   - **Resolution:** 90 meters (global) or 30 meters (US)
   - **Coverage:** Near global
   - **Cost:** Free
   - **Best for:** Legacy support or fallback.

## How to Download Copernicus DEM

Since the Copernicus DEM files are large, FortSight AI does not download them automatically on startup. You must download the region you need manually.

1. **Access Copernicus Data Space Ecosystem:**
   - Go to [Copernicus Data Space](https://dataspace.copernicus.eu/) or [OpenTopography](https://opentopography.org/).
2. **Search for your region:**
   - E.g., for Maharashtra forts (like Rajgad), search for coordinates around `18.67° N, 73.33° E`.
3. **Select Dataset:**
   - Choose the "Copernicus DEM GLO-30" dataset.
4. **Download File:**
   - Download the file as a `GeoTIFF` (`.tif`).
   - Place the file inside the project directory: `backend/data/dem/`

*Example File Name: `Copernicus_DSM_COG_10_N18_00_E073_00_DEM.tif`*

## Ingesting the DEM into FortSight AI

Once you have downloaded the GeoTIFF file, you need to register it in the FortSight AI database so the terrain engine can find it using PostGIS spatial queries.

Run the ingestion script from the `backend` directory:

```bash
# Ensure your virtual environment is active
# e.g., venv\Scripts\activate

python scripts/ingest_dem.py --source copernicus --region maharashtra --file data/dem/Copernicus_DSM_COG_10_N18_00_E073_00_DEM.tif
```

### What the script does:
1. Reads the GeoTIFF file using `rasterio`.
2. Extracts the bounding box (spatial extent) of the DEM.
3. Calculates the resolution.
4. Creates a `terrain_tiles` record in the database with the file path and a PostGIS polygon representing the coverage area.

## Verifying the Terrain Engine

After ingesting the DEM, you can verify it by hitting the API endpoint.
Ensure your FastAPI server is running:

```bash
uvicorn app.main:app --reload
```

Test the endpoint with curl (or in your browser):

```bash
curl "http://localhost:8000/api/v1/terrain/elevation?lat=18.2435&lon=73.6521"
```

You should see a response like this:
```json
{
  "elevation_m": 1376.45,
  "accuracy_m": 30.0,
  "source": "copernicus",
  "confidence": "high"
}
```
