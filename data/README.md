# FortSight AI Data Sourcing and Validation

This directory contains the initial dataset for the FortSight AI MVP, providing data for 10 forts in Maharashtra, including coordinates, elevation, history, viewpoints, and trails.

## Data Source Attribution
- **Coordinates & Elevations**: The latitude, longitude, and elevation points have been sourced from real-world data references (Wikipedia, OpenStreetMap data, and PeakVisor).
- **Historical Data**: Summaries of historical events and fort significance have been curated from standard encyclopedic sources.

## Manual Data Entry Guide

If you need to add more forts, viewpoints, or trails to the system, follow these guidelines:

### 1. `forts_mvp.csv` Format Specification
When adding new rows to the `forts_mvp.csv` file, ensure the following columns are populated correctly:
- `name` (String): The English name of the fort.
- `marathi_name` (String): The Marathi name of the fort.
- `latitude` (Float): Decimal degrees format. Must be between 15.6 and 22.0.
- `longitude` (Float): Decimal degrees format. Must be between 72.6 and 80.9.
- `elevation` (Integer): Height above sea level in meters. (Max 2000m).
- `district` (String): District name in Maharashtra.
- `difficulty` (String): 'Easy', 'Moderate', or 'Hard'.
- `best_season` (String): Best time to visit (e.g., 'Monsoon', 'Winter').
- `history` (String): Brief historical description.
- `image_url` (String): Direct URL to a representational image.
- `source` (String): Provide the attribution of the data source.

### 2. `viewpoints.csv` Format Specification
- `fort_name` (String): Must perfectly match a `name` from `forts_mvp.csv`.
- `name` (String): The name of the viewpoint/machi.
- `latitude` (Float): Viewpoint specific latitude.
- `longitude` (Float): Viewpoint specific longitude.
- `description` (String): Short description of the viewpoint.

### 3. `trails.csv` Format Specification
- `fort_name` (String): Must perfectly match a `name` from `forts_mvp.csv`.
- `name` (String): Trail name or start point.
- `distance_km` (Float): Distance of the trail in kilometers.
- `estimated_time_mins` (Integer): Estimated hiking time in minutes.
- `difficulty` (String): 'Easy', 'Moderate', or 'Hard'.
- `geometry` (String): WKT (Well-Known Text) representation of a LineString. E.g., `LINESTRING(73.6822 18.2461, 73.6850 18.2500)`

## Validation Rules
The import script `scripts/import_forts.py` applies the following hard constraints:
1. Coordinates must fall inside the bounding box of Maharashtra.
2. Elevation cannot be less than 0m or greater than 2000m (Kalsubai is ~1646m).
3. The `source` column must not be empty.
4. If an error is encountered during database insertion (like unique constraint violation or malformed data), the entire transaction is rolled back to prevent dirty reads.
