# Architecture Overview

FortSight AI is designed for robust geospatial analysis and AI-driven insights, utilizing a modern, decoupled microservices-like architecture.

## System Components

### 1. Frontend (React SPA)
- **Framework:** React 18, Vite.
- **Mapping:** React-Leaflet integrated with custom map tiles.
- **State Management:** React Query for data fetching and caching.
- **Serving:** Nginx (in production) for fast static file serving and reverse proxying to the backend.

### 2. Backend (FastAPI)
- **Framework:** FastAPI (Python 3.11).
- **Server:** Gunicorn utilizing `UvicornWorker` for asynchronous request handling.
- **Core Modules:**
  - `gis/`: Spatial analytics, DEM processing using Rasterio/GeoPandas.
  - `ml/`: RAG implementations and Embedding generation using Sentence-Transformers.
  - `api/`: RESTful endpoints.

### 3. Database Layer
- **Relational DB:** PostgreSQL.
- **Vector DB:** `pgvector` extension for storing and querying AI embeddings.
- **ORM:** SQLAlchemy for robust query construction and migrations (Alembic).

### 4. Caching Layer
- **Redis:** Used for caching frequent API queries, rate limiting (SlowAPI), and potentially session management.

## Security Architecture

- **CORS:** Strictly defined origins.
- **Rate Limiting:** IP-based request throttling using Redis.
- **User Permissions:** Non-root users executing inside Docker containers.
- **Environment Management:** Hard separation of `.env` configurations ensuring no secrets leak into logs.

## Performance Enhancements
- Gzip compression enabled on Nginx.
- Multi-stage Docker builds reducing image sizes from gigabytes down to megabytes.
- Connection pooling natively managed by SQLAlchemy.
