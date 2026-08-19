# FortSight AI

A terrain-aware spatial intelligence system for line-of-sight visibility calculations between forts in Maharashtra.

## Repository Structure

- `/frontend` - React + Vite + MapLibre GL JS frontend
- `/backend` - FastAPI backend for spatial analysis
- `/data` - Static data (DEM chunks, GeoJSONs)
- `/scripts` - Utilities for data ingestion
- `/tests` - Pytest test suite
- `/docs` - Project documentation

## Quickstart (Docker)

To run the full stack locally:

1. Copy environment variables:
   ```bash
   cp .env.example .env
   ```

2. Start the services:
   ```bash
   make build
   ```

3. Access the services:
   - **Frontend**: http://localhost:5173
   - **Backend API**: http://localhost:8000/docs
   - **pgAdmin**: http://localhost:5050
