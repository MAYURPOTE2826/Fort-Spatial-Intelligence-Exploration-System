# FortSight AI - Phase-Wise AI Prompts
## Step-by-Step Guide to Build the Complete Project

---

## PHASE 0: Feasibility & Architecture Analysis

### Goal
Understand the entire system, identify risks, define MVP scope, and create the architecture blueprint.

### Prompt for AI Assistant:

```
CONTEXT:
I am building FortSight AI - a real-time terrain-aware spatial intelligence 
system that determines which forts are visible from a user's exact GPS location, 
considering terrain obstruction, device orientation, and elevation.

REGION: Maharashtra, India
FORTS: ~10 initial forts (Rajgad, Torna, Sinhagad, Purandar, Lohagad, 
        Visapur, Raigad, Pratapgad, Shivneri, Tikona)

TASK:
1. Assess technical feasibility of terrain-aware line-of-sight visibility calculation
2. Identify data requirements (DEM source, fort coordinates, elevation data)
3. List technical risks and mitigation strategies
4. Define minimal MVP that works WITHOUT ML/RAG
5. Create high-level system architecture
6. Justify technology choices for:
   - Frontend: React + TypeScript + Leaflet/MapLibre
   - Backend: FastAPI + PostgreSQL + PostGIS
   - GIS: GDAL, Rasterio, GeoPandas
   - Terrain: SRTM/Copernicus DEM

OUTPUT REQUIRED:
- Feasibility assessment (2-3 pages)
- Technical risks & mitigation
- MVP definition (what must work vs. what's future)
- Architecture diagram (Mermaid)
- Data sourcing strategy (DEM, fort coords, elevation)
- Technology stack justification
- Estimated effort breakdown by phase
```

### Deliverables to Expect:
- System feasibility report
- Architecture diagram in Mermaid
- MVP scope definition
- Risk register
- Data sourcing checklist

### When Complete: Proceed to Phase 1

---

## PHASE 1: Repository Setup & Docker Foundation

### Goal
Create production-ready monorepo structure with Docker configuration and development environment.

### Prompt for AI Assistant:

```
CONTEXT:
FortSight AI is a full-stack terrain-aware fort visibility system.
Project will use:
- Frontend: React + TypeScript + Vite
- Backend: FastAPI + Python
- Database: PostgreSQL + PostGIS
- Deployment: Docker + Docker Compose

TASK:
Create a professional monorepo with complete Docker setup for development.

REQUIREMENTS:
1. Create folder structure:
   /frontend - React Vite app
   /backend - FastAPI application
   /data - DEM, forts, trails, documents
   /scripts - data ingestion, utilities
   /tests - pytest tests
   /docs - documentation

2. Create Docker configuration:
   - Dockerfile.frontend (Node 18, Vite)
   - Dockerfile.backend (Python 3.11, FastAPI)
   - docker-compose.yml with:
     * PostgreSQL 15 + PostGIS
     * FastAPI backend
     * React frontend (dev mode)
     * pgAdmin (optional, for development)
     * Redis (optional, for caching)

3. Create environment files:
   - .env.example
   - .env.development.example

4. Create supporting files:
   - Makefile with development commands
   - .gitignore
   - README.md (skeleton)
   - docker-compose.override.yml for local development

5. Frontend initialization:
   - package.json with dependencies
   - vite.config.ts
   - tsconfig.json
   - tailwind.config.js
   - postcss.config.js
   - Basic app structure ready for maps

6. Backend initialization:
   - requirements.txt with all dependencies
   - FastAPI app/main.py scaffold
   - app/core/config.py for settings
   - app/core/database.py for DB connection
   - Logging configuration
   - Environment variable handling

7. Documentation:
   - Docker setup instructions
   - First-time developer setup guide
   - Command reference (Makefile)
   - Folder structure explanation

IMPORTANT:
- No hardcoded secrets (use .env)
- Make it work on Linux/Mac/Windows
- Include health check endpoints
- Production-ready Docker best practices
- Development hot-reload ready

OUTPUT:
Provide complete file listings and exact commands to:
1. Clone/setup repo
2. Build Docker images
3. Start development environment
4. Test that services are running
```

### Deliverables:
- Complete monorepo structure
- Docker + Docker Compose setup
- .env examples
- Makefile
- README with setup instructions
- First working Docker development environment

### Verification:
```bash
docker-compose up
# Should start PostgreSQL, FastAPI, React without errors
# Frontend accessible at http://localhost:5173
# Backend accessible at http://localhost:8000
```

### When Complete: Proceed to Phase 2

---

## PHASE 2: PostgreSQL + PostGIS Database Design

### Goal
Design and implement normalized PostgreSQL database schema with PostGIS extensions.

### Prompt for AI Assistant:

```
CONTEXT:
FortSight AI backend uses PostgreSQL + PostGIS.
Database stores: forts, viewpoints, trails, terrain metadata, historical documents,
visibility cache, user sessions, and chat messages.

TASK:
Create complete database schema with:

1. Core tables:
   - users (id, name, email, created_at, updated_at)
   - forts (id, name, marathi_name, description, geometry(Point), 
            elevation, district, difficulty, best_season, history, 
            image_url, source, created_at, updated_at)
   - fort_viewpoints (id, fort_id, name, type, geometry(Point), 
                      elevation, description, created_at)
   - fort_structures (id, fort_id, name, type, geometry(Point/Polygon), 
                      description, created_at)
   - fort_trails (id, fort_id, name, difficulty, geometry(LineString), 
                  distance_km, estimated_time_hours, created_at)
   - fort_connections (source_fort_id, target_fort_id, distance_km, 
                       bearing_deg, visibility_status, visibility_score, 
                       last_calculated_at)

2. Terrain tables:
   - terrain_tiles (id, tile_name, zoom_level, geometry, file_path, 
                    resolution_m, created_at)

3. RAG/Chatbot tables:
   - historical_documents (id, title, content, source_url, fort_id, 
                          created_at, updated_at)
   - document_chunks (id, document_id, chunk_index, content, embedding, 
                      created_at)
   - chat_sessions (id, user_id, created_at, updated_at)
   - chat_messages (id, session_id, role, content, latitude, longitude, 
                    heading, created_at)

4. Visibility cache:
   - visibility_results (id, observer_lat, observer_lon, observer_elevation,
                         fort_id, visibility_status, visibility_score,
                         calculated_at, expires_at)

REQUIREMENTS:
1. Create Alembic migration structure
2. Define all tables with proper data types
3. Add PostGIS geometry columns
4. Create indexes for:
   - Spatial queries (GIST indexes)
   - Fort lookups
   - Visibility cache expiration
   - Document search
5. Add constraints and validations
6. Document index strategy
7. Provide sample data loading script
8. Create raw SQL for schema review
9. SQLAlchemy model definitions
10. Pydantic schemas for API responses

IMPORTANT:
- Use SRID 4326 (WGS84) for all geometries
- Index fort locations spatially
- Cache visibility results with TTL
- Document source attribution in schema
- Support Marathi text (UTF-8)

OUTPUT:
1. Alembic migration files (001_initial_schema.py)
2. SQLAlchemy models (models/fort.py, models/visibility.py, etc.)
3. Pydantic schemas (schemas/fort.py, schemas/visibility.py)
4. Database initialization script
5. Index strategy document
6. Sample data loading script
```

### Deliverables:
- SQLAlchemy models for all tables
- Alembic migration files
- Pydantic schemas
- Database initialization script
- Raw SQL schema dump
- Index documentation

### Verification:
```bash
# Run migrations
alembic upgrade head

# Check schema created
psql -d fortsight_db -c "\dt"  # Should show all tables
psql -d fortsight_db -c "\di"  # Should show indexes

# Test PostGIS
psql -d fortsight_db -c "SELECT PostGIS_Version();"
```

### When Complete: Proceed to Phase 3

---

## PHASE 3: Fort Data Ingestion Pipeline

### Goal
Create scripts to import Maharashtra forts data into PostgreSQL.

### Prompt for AI Assistant:

```
CONTEXT:
FortSight AI needs initial dataset of ~10 Maharashtra forts for MVP.
Data includes: coordinates, elevation, names (English + Marathi), 
descriptions, images, difficulty levels.

TASK:
Create data ingestion pipeline:

1. Prepare MVP fort dataset:
   - Rajgad (18.6753°N, 73.3289°E, ~1400m)
   - Torna (18.7336°N, 73.2639°E, ~1400m)
   - Sinhagad (18.7669°N, 73.3044°E, ~760m)
   - Purandar (18.5519°N, 73.8978°E, ~1100m)
   - Lohagad (18.7639°N, 73.4253°E, ~1050m)
   - Visapur (18.7517°N, 73.4436°E, ~750m)
   - Raigad (18.1939°N, 73.2761°E, ~800m)
   - Pratapgad (17.4172°N, 73.3367°E, ~3500m)
   - Shivneri (19.1406°N, 74.1783°E, ~700m)
   - Tikona (18.4869°N, 73.4331°E, ~1200m)

2. Create data files:
   - CSV: forts_mvp.csv with columns:
     name, marathi_name, latitude, longitude, elevation, 
     district, difficulty, best_season, history, image_url, source
   - GeoJSON: forts_mvp.geojson
   - Sample historical documents (Markdown)

3. Create import script (scripts/import_forts.py):
   - Read CSV/GeoJSON
   - Validate coordinates (valid lat/lon ranges)
   - Check for duplicates
   - Validate geometry
   - Verify elevation data
   - Check source attribution
   - Handle errors gracefully
   - Provide logging
   - Rollback on error

4. Create viewpoints data:
   - Sample viewpoints for each fort
   - Store as CSV
   - Import script included

5. Create trails data:
   - Trail information (geometry as LineString)
   - Distance, estimated time, difficulty
   - CSV + import script

6. Documentation:
   - Data source attribution
   - Manual data entry guide
   - CSV format specification
   - Validation rules
   - How to add new forts

IMPORTANT:
- Do NOT fabricate coordinates (research real data)
- Do NOT make up elevation (use DEM later)
- Provide source attribution
- Make data extensible
- Include validation

OUTPUT:
1. Fort data files (CSV, GeoJSON)
2. Viewpoints data file
3. Trails data file
4. import_forts.py script (complete, production-ready)
5. Data source documentation
6. Manual entry guide
```

### Deliverables:
- forts_mvp.csv with real Maharashtra fort data
- forts_mvp.geojson
- viewpoints.csv
- trails.csv
- scripts/import_forts.py
- scripts/import_viewpoints.py
- scripts/import_trails.py
- data/README.md (sourcing guide)

### Verification:
```bash
# Run import
python scripts/import_forts.py

# Check database
psql -d fortsight_db -c "SELECT name, elevation FROM forts ORDER BY name;"

# Should show 10 forts with proper data
```

### When Complete: Proceed to Phase 4

---

## PHASE 4: FastAPI Core Application Structure

### Goal
Build production-ready FastAPI application with all core infrastructure.

### Prompt for AI Assistant:

```
CONTEXT:
Building FortSight AI backend with FastAPI.
Needs: authentication, dependency injection, error handling, 
logging, environment configuration, database connection.

TASK:
Create complete FastAPI application structure:

1. Core infrastructure:
   app/main.py - FastAPI app setup
   app/core/config.py - environment variables
   app/core/database.py - SQLAlchemy connection pool
   app/core/security.py - JWT, CORS, auth
   app/core/logging.py - structured logging
   app/utils/errors.py - custom exception classes
   app/utils/validators.py - input validation

2. API structure:
   app/api/v1/router.py - route aggregator
   app/api/v1/endpoints/ - endpoint modules
     - health.py (GET /health, /ready)
     - forts.py (fort CRUD)
     - visibility.py (visibility calculations)
     - terrain.py (terrain elevation)
     - routes.py (trekking routes)
     - chat.py (RAG chatbot)
     - auth.py (authentication)

3. Database layer:
   app/models/ - SQLAlchemy models
   app/schemas/ - Pydantic schemas
   app/repositories/ - data access layer

4. Services:
   app/services/fort_service.py
   app/services/visibility_service.py
   app/services/terrain_service.py
   app/services/chat_service.py

5. Middleware:
   - CORS configuration
   - Request logging
   - Error handling
   - Rate limiting
   - Request ID tracking

6. Configuration:
   - Environment variables (.env)
   - Different configs for dev/prod
   - Database URL management
   - LLM provider keys (placeholder)

7. Testing setup:
   - conftest.py for pytest
   - Test database setup
   - Mock fixtures

8. Documentation:
   - API endpoints (OpenAPI auto-generated)
   - Setup instructions
   - Configuration guide
   - Development workflow

IMPORTANT:
- Type hints everywhere
- Async/await ready
- Proper error responses
- No secrets in code
- Structured logging
- Health check endpoints
- Request validation
- CORS properly configured

OUTPUT:
1. Complete app/ directory structure
2. main.py with FastAPI initialization
3. All core modules (config, database, security)
4. Endpoint stubs for all major features
5. Error handling middleware
6. Logging configuration
7. Database connection pool setup
8. Docker integration verified
9. OpenAPI documentation working
```

### Deliverables:
- app/main.py
- app/core/ (config, database, security, logging)
- app/api/v1/ (router + stub endpoints)
- app/models/, app/schemas/, app/repositories/ (stubs)
- requirements.txt (complete)
- .env.example (complete)
- docker-compose.yml (updated)

### Verification:
```bash
# Start container
docker-compose up backend

# Check health
curl http://localhost:8000/health

# View OpenAPI docs
# Navigate to http://localhost:8000/docs
```

### When Complete: Proceed to Phase 5

---

## PHASE 5: Terrain Engine (DEM Processing)

### Goal
Implement Digital Elevation Model (DEM) handling and terrain elevation queries.

### Prompt for AI Assistant:

```
CONTEXT:
FortSight AI needs terrain elevation data for line-of-sight calculations.
Uses SRTM or Copernicus DEM data.
Must query elevation at any lat/lon point.

TASK:
Build terrain engine:

1. DEM source selection & download guide:
   - Copernicus DEM (30m resolution, global, free)
   - NASA SRTM (90m resolution)
   - How to download
   - Expected file format
   - Storage location

2. DEM preprocessing:
   app/gis/dem_processor.py:
   - Load GeoTIFF DEM files
   - Reproject to EPSG:4326 (WGS84)
   - Validate raster properties
   - Handle nodata values
   - Create tile index (spatial index for fast lookups)
   - Cache tiles in memory / on disk
   - Provide elevation query function

3. Terrain service:
   app/services/terrain_service.py:
   - Query elevation at (lat, lon)
   - Interpolate between grid points
   - Handle cache
   - Provide confidence/accuracy info
   - Error handling for out-of-bounds
   - Support multiple DEM sources

4. DEM ingestion script:
   scripts/ingest_dem.py:
   - Download Copernicus DEM for Maharashtra
   - Process and cache locally
   - Create spatial index
   - Store metadata in database
   - Provide progress tracking

5. Database support:
   - terrain_tiles table (stores DEM metadata)
   - DEM file paths
   - Resolution info
   - Created/updated timestamps

6. Caching strategy:
   - In-memory LRU cache for recent queries
   - Disk cache for DEM tiles
   - TTL for cache expiration
   - Cache hit/miss logging

7. API endpoint:
   GET /api/v1/terrain/elevation
   Parameters: lat, lon
   Response: { elevation_m, accuracy_m, source, confidence }

8. Testing:
   - Unit tests for elevation queries
   - Interpolation accuracy tests
   - Cache behavior tests
   - Error handling tests

IMPORTANT:
- Do NOT download DEM automatically on startup
- Provide manual ingestion command
- Support multiple DEM sources
- Proper error handling for invalid coordinates
- Efficient interpolation algorithm
- Document DEM source and accuracy

OUTPUT:
1. app/gis/dem_processor.py (complete)
2. app/services/terrain_service.py (complete)
3. scripts/ingest_dem.py (with instructions)
4. Configuration for DEM paths
5. Testing suite (unit tests)
6. Documentation on DEM source and usage
7. API endpoint implementation
8. Database schema for terrain metadata
```

### Deliverables:
- DEM processor module
- Terrain service with elevation queries
- Ingestion script with instructions
- API endpoint
- Unit tests
- Documentation

### Verification:
```bash
# After manually placing DEM file
python scripts/ingest_dem.py --source copernicus --region maharashtra

# Test endpoint
curl "http://localhost:8000/api/v1/terrain/elevation?lat=18.67&lon=73.33"

# Should return elevation for Rajgad area (~1400m)
```

### When Complete: Proceed to Phase 6

---

## PHASE 6: Visibility Engine (Line-of-Sight Algorithm)

### Goal
Implement terrain-aware line-of-sight visibility calculation algorithm.

### Prompt for AI Assistant:

```
CONTEXT:
Core innovation of FortSight AI.
Determines if a fort is visible from observer location considering:
- Geodesic distance
- Bearing/direction
- Observer elevation + height
- Fort elevation + height
- Terrain obstruction between observer and fort

TASK:
Implement visibility engine:

1. Core algorithm:
   app/gis/visibility_engine.py:
   
   Function: calculate_line_of_sight(
       observer_lat, observer_lon, observer_elevation, observer_height,
       target_lat, target_lon, target_elevation, target_height,
       dem_service
   ) -> VisibilityResult
   
   Algorithm steps:
   a. Calculate geodesic distance using Haversine or Vincenty
   b. Calculate bearing using atan2
   c. Generate sample points along line (every 100m or based on distance)
   d. For each sample point:
      - Interpolate terrain elevation from DEM
      - Calculate expected line-of-sight elevation
      - Compare terrain vs. sightline
   e. Detect maximum obstruction
   f. Calculate visibility score (0-1)
   g. Return detailed result

2. Visibility score calculation:
   - Factor 1: Terrain clearance (how much above terrain)
   - Factor 2: Distance (farther = lower confidence)
   - Factor 3: Observer height above terrain
   - Mathematical formula (document clearly)
   - Score 0.9+ = VISIBLE
   - Score 0.5-0.9 = UNCERTAIN
   - Score < 0.5 = BLOCKED

3. Result structure:
   class VisibilityResult:
       fort_id: str
       distance_km: float
       bearing_deg: float
       direction: str  # N, NE, E, etc.
       observer_elevation: float
       target_elevation: float
       max_terrain_intersection: float  # elevation of obstruction
       visibility_status: str  # VISIBLE, BLOCKED, UNCERTAIN
       visibility_score: float  # 0.0-1.0
       obstruction_distance_km: Optional[float]  # how far until blocked
       confidence: float  # how confident in result
       explanation: str  # human readable

4. Direction engine:
   app/gis/direction_engine.py:
   - Convert bearing (0-360°) to cardinal direction (N, NE, E, etc.)
   - Calculate relative angle to user heading
   - Determine if fort is in field of view (configurable FOV, default 60°)
   - Return direction string

5. Performance optimization:
   - Sample point optimization (adaptive sampling based on distance)
   - DEM query batching
   - Result caching
   - Parallel processing for multiple targets

6. Testing:
   - Known visibility cases (test scenarios)
   - Bearing calculation accuracy
   - Direction conversion
   - Score calculation validation
   - Edge cases (observer in valley, mountain peak, etc.)

7. Documentation:
   - Algorithm explanation
   - Assumptions and limitations
   - Accuracy discussion
   - Sample calculations
   - Known issues

IMPORTANT:
- NO fake visibility scores
- Document all mathematical formulas
- Explain assumptions clearly
- Provide test cases
- Handle edge cases
- Cache results for performance
- Validate all inputs

OUTPUT:
1. app/gis/visibility_engine.py (complete algorithm)
2. app/gis/direction_engine.py (bearing to direction)
3. Comprehensive algorithm documentation
4. Unit tests with known cases
5. Performance benchmarks
6. Result schema/dataclass
7. Edge case handling
```

### Deliverables:
- Visibility engine module
- Direction engine module
- Algorithm documentation
- Comprehensive test suite
- Performance benchmarks
- Result schemas

### Verification:
```bash
# Run test suite
pytest app/gis/test_visibility_engine.py -v

# Should show algorithm working correctly
# Example: Rajgad -> Torna should be VISIBLE (historically viewable)
# Example: Rajgad -> Fort on other side of mountain should be BLOCKED
```

### When Complete: Proceed to Phase 7

---

## PHASE 7: Visibility API Endpoint

### Goal
Expose visibility calculation as REST API with optimization and caching.

### Prompt for AI Assistant:

```
CONTEXT:
Visibility engine implemented. Now expose via REST API.
Must handle multiple forts, spatial filtering, caching, performance.

TASK:
Build visibility API:

1. Main endpoint:
   GET /api/v1/visibility/from-location
   
   Query parameters:
   - lat (float, required): observer latitude
   - lon (float, required): observer longitude
   - heading (float, optional): compass heading (0-360)
   - fov (float, optional): field of view in degrees (default 60)
   - radius_km (float, optional): search radius (default 50)
   - elevation (float, optional): observer elevation above ground
   - observer_height (float, optional): observer height (eyes above ground, default 1.7m)
   
   Response:
   {
     "observer": {
       "lat": 18.67,
       "lon": 73.33,
       "elevation": 1400,
       "heading": 245
     },
     "visible_forts": [
       {
         "id": "torna",
         "name": "Torna",
         "distance_km": 12.4,
         "bearing_deg": 245,
         "direction": "SW",
         "relative_angle": 15,
         "visibility_score": 0.91,
         "visibility_status": "VISIBLE",
         "elevation": 1400,
         "elevation_difference": 0,
         "image_url": "..."
       }
     ],
     "uncertain_forts": [...],
     "blocked_forts": [...],
     "calculation_time_ms": 145
   }

2. Fort-to-fort endpoint:
   POST /api/v1/visibility/between-forts
   
   Request:
   {
     "source_fort_id": "rajgad",
     "target_fort_id": "torna"
   }
   
   Response: Same VisibilityResult structure

3. Visibility network endpoint:
   POST /api/v1/visibility/build-network
   
   Request:
   {
     "fort_ids": ["rajgad", "torna", "sinhagad", ...]
   }
   
   Response: Graph of fort-to-fort visibility relationships

4. Optimization strategy:
   a. Spatial filtering (PostGIS):
      - Query forts within radius using PostGIS
      - Eliminate distant forts before DEM queries
   
   b. Caching:
      - Cache visibility results in database
      - TTL: 24 hours (or configurable)
      - Cache key: (lat, lon, heading, fov)
      - Invalidate on DEM updates
   
   c. Performance enhancement:
      - Async processing for multiple forts
      - Batch DEM queries
      - Parallel visibility calculations
      - Use Celery/RQ if needed for network building

5. Request validation:
   - Latitude range: -90 to 90
   - Longitude range: -180 to 180
   - Heading: 0-360
   - FOV: 1-180
   - Radius: 1-200 km
   - Elevation: reasonable range

6. Error handling:
   - Invalid coordinates
   - No DEM data available
   - No forts in radius
   - Database errors
   - Timeout errors
   - Clear error messages

7. Rate limiting:
   - Limit requests per IP (configurable)
   - Longer limit for network endpoint
   - Provide rate limit headers

8. Logging:
   - Log all requests
   - Log calculation time
   - Log cache hits/misses
   - Log errors with context

9. Testing:
   - Unit tests for endpoint
   - Integration tests
   - Performance tests
   - Load testing
   - Edge cases

IMPORTANT:
- Optimize for mobile (small payloads)
- Return only necessary data
- Cache aggressively
- Handle slow clients
- Provide calculation time feedback

OUTPUT:
1. app/api/v1/endpoints/visibility.py (complete)
2. app/services/visibility_service.py (with caching)
3. Caching strategy documentation
4. Performance optimization guide
5. API documentation
6. Integration tests
7. Load testing script
```

### Deliverables:
- Visibility API endpoint (complete)
- Service layer with caching
- Database visibility cache table
- Rate limiting
- Comprehensive tests
- API documentation

### Verification:
```bash
# Test endpoint
curl "http://localhost:8000/api/v1/visibility/from-location?lat=18.67&lon=73.33&radius_km=50"

# Should return visible/blocked/uncertain forts
# Response should include calculations time
# Should be cached on second call
```

### When Complete: Proceed to Phase 8

---

## PHASE 8: React Map Frontend - Base Setup

### Goal
Build responsive React frontend with interactive map showing forts and user location.

### Prompt for AI Assistant:

```
CONTEXT:
FortSight AI frontend using React + TypeScript + Vite + Leaflet.
Mobile-first design for trekkers.
Dark theme with terrain-inspired colors.

TASK:
Build base frontend application:

1. Project structure:
   frontend/src/
   ├── components/
   │   ├── Map.tsx
   │   ├── FortMarker.tsx
   │   ├── LocationMarker.tsx
   │   ├── DirectionArrow.tsx
   │   ├── FortList.tsx
   │   ├── LocationPanel.tsx
   │   ├── Header.tsx
   │   └── ui/ (shadcn components)
   ├── pages/
   │   ├── MapPage.tsx
   │   ├── FortDetailsPage.tsx
   │   ├── AboutPage.tsx
   │   └── NotFoundPage.tsx
   ├── hooks/
   │   ├── useLocation.ts
   │   ├── useHeading.ts
   │   ├── useForts.ts
   │   └── useVisibility.ts
   ├── services/
   │   ├── api.ts
   │   ├── geoService.ts
   │   └── cacheService.ts
   ├── types/
   │   ├── fort.ts
   │   ├── visibility.ts
   │   └── location.ts
   ├── utils/
   │   ├── bearingToDirection.ts
   │   ├── formatDistance.ts
   │   └── colorScheme.ts
   ├── App.tsx
   └── main.tsx

2. Core components:
   a. Map component:
      - Leaflet map
      - Show user location
      - Show fort markers
      - Show heading arrow
      - Show visibility lines
      - Click fort for details
      - Responsive sizing
   
   b. Location panel:
      - Current latitude/longitude
      - Current elevation
      - Current heading
      - Search location input
      - Location accuracy
      - Update interval
   
   c. Fort list:
      - Visible forts (highlighted)
      - Uncertain forts
      - Blocked forts
      - Sort by distance/direction
      - Click to see details
      - Show visibility score
   
   d. Direction arrow:
      - Point to user heading
      - Rotate as user turns
      - Show FOV cone (optional)
      - Updates in real-time

3. Styling:
   - Dark theme (terrain-inspired)
   - Color scheme:
     * Visible: Green/emerald
     * Uncertain: Amber/yellow
     * Blocked: Red/gray
     * Terrain: Browns/earth tones
   - Responsive layout (mobile-first)
   - Tailwind CSS + custom theme
   - Lucide icons

4. State management:
   - React Query for API data
   - React Context for user location
   - Local state for UI
   - Session storage for preferences

5. API integration:
   - Base API client with error handling
   - Endpoints for:
     * GET /health (check backend)
     * GET /api/v1/forts (list all)
     * GET /api/v1/visibility/from-location
     * GET /api/v1/forts/{id}
   - Request/response types
   - Error handling
   - Retry logic

6. Performance:
   - Code splitting
   - Lazy loading pages
   - Memoization of components
   - Efficient re-renders
   - Local data caching

7. Accessibility:
   - Semantic HTML
   - ARIA labels
   - Keyboard navigation
   - Color contrast
   - Mobile-friendly touch targets

8. Testing setup:
   - Vitest configuration
   - React Testing Library setup
   - Mock API responses

9. Documentation:
   - Component API
   - Hook usage
   - Service integration
   - Development guide

IMPORTANT:
- Mobile-first responsive design
- Dark theme
- Fast load times
- Proper TypeScript types
- No hardcoded API URLs
- Accessible to all users
- Intuitive UX for trekkers

OUTPUT:
1. Complete frontend structure
2. Base components (Map, LocationPanel, FortList)
3. React Query setup
4. API service layer
5. Type definitions
6. Tailwind theme configuration
7. Dark theme configuration
8. Build configuration (Vite)
9. Dev environment working
10. Component tests
```

### Deliverables:
- Complete React project structure
- Leaflet map integration
- Location and heading panels
- Fort list component
- API service layer
- Type definitions
- Tailwind + dark theme

### Verification:
```bash
cd frontend
npm install
npm run dev

# Open http://localhost:5173
# Should show map, fort markers, location panel
# Dark theme applied
# Responsive on mobile
```

### When Complete: Proceed to Phase 9

---

## PHASE 9: GPS & Device Orientation Integration

### Goal
Capture real GPS location and compass heading from device.

### Prompt for AI Assistant:

```
CONTEXT:
FortSight AI uses real GPS and device orientation to show forts.
Need to access device APIs safely with fallback for desktop.

TASK:
Implement location and orientation:

1. GPS Location API:
   hook: useLocation()
   
   Returns:
   {
     latitude: number
     longitude: number
     accuracy: number (meters)
     altitude: number
     timestamp: number
     loading: boolean
     error: string | null
   }
   
   Features:
   - Request permission on first load
   - Handle permission denied
   - High accuracy mode
   - Watch position updates (1-2 Hz)
   - Fallback to manual entry on desktop
   - Display accuracy circle
   - Stop watching on unmount

2. Compass Heading API:
   hook: useHeading()
   
   Returns:
   {
     heading: number (0-360°)
     accuracy: number (degrees)
     timestamp: number
     loading: boolean
     error: string | null
   }
   
   Features:
   - Use Device Orientation API
   - Request permission (iOS 13+)
   - Handle denied permission
   - Smooth heading updates (60+ Hz)
   - Fallback to manual input on desktop
   - Magnetic vs true north handling
   - Stop watching on unmount

3. Desktop development:
   - Manual location input form
   - Manual heading slider (0-360°)
   - Simulate GPS accuracy
   - Simulate heading updates
   - Dev panel to change location/heading

4. Location permissions UI:
   - Permission request dialog
   - Explain why location is needed
   - Fallback when denied
   - Links to settings
   - Privacy statement

5. Accuracy display:
   - Accuracy circle on map
   - Heading confidence indicator
   - Age of data
   - Update frequency display

6. Performance:
   - Debounce API calls
   - Cache location updates
   - Batch updates
   - Stop updates when not in focus
   - Clean up on unmount

7. Error handling:
   - No location permission
   - Location timeout
   - No compass hardware
   - Inaccurate heading
   - Clear error messages

8. Testing:
   - Mock geolocation API
   - Mock orientation API
   - Test permission flows
   - Test fallback behavior
   - Test error scenarios

9. Documentation:
   - How to use hooks
   - Permission handling
   - Desktop development
   - Accuracy considerations
   - Privacy statement template

IMPORTANT:
- Ask for permission first
- Don't force it
- Fallback for desktop dev
- Show accuracy/confidence
- Stop updates when not needed
- Handle permission denied gracefully
- Privacy-first approach

OUTPUT:
1. useLocation() hook (complete)
2. useHeading() hook (complete)
3. DevLocationPanel component (desktop dev)
4. Permission request dialog
5. Accuracy display components
6. Integration with map
7. Type definitions
8. Tests for hooks
9. Error handling
10. Privacy documentation
```

### Deliverables:
- useLocation hook with real GPS
- useHeading hook with compass
- Permission handling
- Desktop dev panel
- Accuracy display
- Integration with map
- Comprehensive tests

### Verification:
```bash
# On mobile device:
# - App requests location permission
# - App requests orientation permission
# - Map shows your location
# - Heading arrow updates as you rotate device
# - Visible forts update when you move

# On desktop:
# - Dev panel shows location/heading inputs
# - Can manually change coordinates
# - Map updates in real-time
```

### When Complete: Proceed to Phase 10

---

## PHASE 10: Fort Internal Maps & Details

### Goal
Display detailed information for each fort including internal structures and viewpoints.

### Prompt for AI Assistant:

```
CONTEXT:
Users click on fort to see internal map with structures, viewpoints, trails.
Display historical information and images.

TASK:
Implement fort details:

1. Fort details page:
   Pages/FortDetailsPage.tsx
   
   Display:
   - Fort name (English + Marathi)
   - High-resolution map (internal)
   - Basic info card:
     * Elevation
     * Distance from you
     * Bearing/direction
     * Visibility status
   - Tabs:
     * Overview (history, description)
     * Map (internal structures)
     * Viewpoints
     * Trails
     * Gallery
     * Related forts

2. Internal fort map:
   Components/FortMap.tsx
   
   Features:
   - Leaflet map of fort area
   - Show fort boundary (polygon)
   - Show structures:
     * Gates (marked with doors)
     * Machis (marked with towers)
     * Bastions
     * Temples (marked with religious symbol)
     * Water tanks
     * Viewpoints (marked with eyes)
   - Show trails
   - Click structures for info
   - Layers toggle (structures, trails, etc.)
   - Satellite view option

3. Structures data:
   Components/StructureInfo.tsx
   
   Display:
   - Structure name
   - Type (gate, machi, bastion, temple, etc.)
   - Description
   - Historical significance
   - Best viewpoint from it
   - Photos if available

4. Viewpoints:
   Components/ViewpointsList.tsx
   
   Display:
   - Popular viewpoints at fort
   - Direction they face
   - What's visible from them
   - Difficulty to reach
   - Time to visit

5. Trails:
   Components/TrailsList.tsx
   
   Display:
   - Trail name
   - Starting point
   - Ending point
   - Distance
   - Estimated time
   - Difficulty level
   - Elevation gain
   - Waypoints/path

6. Fort history:
   Components/FortHistory.tsx
   
   Display:
   - Built by/when
   - Historical events
   - Architectural style
   - Interesting facts
   - Marathi history

7. Gallery:
   Components/FortGallery.tsx
   
   Features:
   - Grid of fort photos
   - Click to fullscreen
   - Photo source attribution
   - Load images lazily

8. Related forts:
   Components/RelatedForts.tsx
   
   Display:
   - Nearby forts
   - Visible from this fort
   - Connected by trails
   - Historical connections

9. API endpoints:
   GET /api/v1/forts/{id}
   GET /api/v1/forts/{id}/structures
   GET /api/v1/forts/{id}/viewpoints
   GET /api/v1/forts/{id}/trails
   GET /api/v1/forts/{id}/connections

10. Navigation:
    - Back to map
    - Share fort info
    - View on external map
    - Directions to fort

IMPORTANT:
- Use real historical data
- Provide accurate coordinates
- Mobile-responsive layout
- Load images efficiently
- Link to data sources
- Support Marathi text

OUTPUT:
1. FortDetailsPage component
2. FortMap component
3. Individual structure/viewpoint/trail components
4. Data models for internal structures
5. Database schema updates (if needed)
6. API endpoints (complete)
7. Type definitions
8. Image loading strategy
9. Navigation integration
```

### Deliverables:
- Fort details page
- Internal fort map
- Structure/viewpoint/trail components
- Related forts component
- Gallery component
- Navigation integration
- API endpoints

### Verification:
```bash
# Click on a fort marker
# Should navigate to /fort/{fort-id}
# Should show:
# - Fort name and elevation
# - Internal map with structures
# - Viewpoints list
# - Trails
# - Historical information
# - Related forts
```

### When Complete: Proceed to Phase 11

---

## PHASE 11: Fort-to-Fort Visibility Network

### Goal
Calculate and display which forts can see each other, creating a visibility graph.

### Prompt for AI Assistant:

```
CONTEXT:
Advanced feature: show relationships between forts.
Which forts can see each other? What's the visibility network?

TASK:
Implement fort visibility network:

1. Backend calculation:
   POST /api/v1/visibility/build-network
   
   Input:
   {
     "fort_ids": ["rajgad", "torna", "sinhagad", ...],
     "async": true (for large networks)
   }
   
   Calculation:
   - For each pair of forts: calculate visibility
   - Store results in fort_connections table
   - Update visibility graph
   - Cache results (TTL: 7 days or until DEM update)
   
   Output:
   {
     "network": {
       "forts": [
         { "id": "rajgad", "name": "Rajgad", ... }
       ],
       "connections": [
         {
           "from": "rajgad",
           "to": "torna",
           "distance_km": 12.4,
           "bearing_deg": 245,
           "visibility": "VISIBLE",
           "score": 0.91
         }
       ]
     },
     "calculation_time_ms": 2340
   }

2. Async job:
   If many forts, run as background job:
   - Celery/RQ task
   - Progress tracking
   - Notification when complete
   - Store in database
   - Cache for reuse

3. Frontend visualization:
   Pages/NetworkPage.tsx
   
   Display:
   - Graph visualization (Force-directed or Hierarchy)
   - Each node = fort
   - Each edge = visibility relationship
   - Edge color = visibility status
     * Green = VISIBLE
     * Amber = UNCERTAIN
     * Red = BLOCKED
   - Edge thickness = visibility score
   - Click node to see fort details
   - Click edge to see details
   - Pan and zoom
   - Search for fort
   - Filter by region

4. Graph library:
   Options:
   - D3.js (powerful, complex)
   - Nivo (easier)
   - Vis.js (good balance)
   - React Flow (node-based UI)
   
   Should support:
   - Force-directed simulation
   - Dynamic updates
   - Interactivity
   - Export as image

5. Network statistics:
   Display:
   - Total forts in network
   - Total visible connections
   - Average visibility per fort
   - Most connected fort
   - Isolated forts
   - Network density

6. Filters:
   - Show only visible connections
   - Show only fort clusters/regions
   - Distance range
   - Visibility score threshold

7. Export options:
   - Export as JSON
   - Export as image
   - Export as GeoJSON

8. Database updates:
   fort_connections table:
   - source_fort_id
   - target_fort_id
   - distance_km
   - bearing_deg
   - visibility_status
   - visibility_score
   - calculated_at

9. Cache invalidation:
   - Invalidate when DEM updated
   - Invalidate when fort data changed
   - Manual invalidation option

10. Performance:
    - Cache network for reuse
    - Lazy load large networks
    - Parallel calculation for pairs
    - Optimize graph rendering

IMPORTANT:
- Reuse existing visibility engine
- Cache network results
- Handle large networks efficiently
- Interactive visualization
- Export capabilities

OUTPUT:
1. Network calculation endpoint (complete)
2. Async job setup (Celery/RQ)
3. Frontend NetworkPage component
4. Graph visualization component
5. Network statistics component
6. Database queries for network
7. Cache strategy
8. Tests
```

### Deliverables:
- Network calculation endpoint
- Async job handling
- Frontend network visualization
- Graph rendering component
- Network statistics
- Export functionality
- Integration tests

### Verification:
```bash
# Build network for MVP forts
POST http://localhost:8000/api/v1/visibility/build-network

# Navigate to network page
# Should show graph visualization
# Nodes = forts, edges = visibility
# Green edges = visible, red = blocked
# Click nodes/edges for details
```

### When Complete: Proceed to Phase 12

---

## PHASE 12: RAG Chatbot

### Goal
Build Marathi-aware RAG chatbot for natural language queries about forts.

### Prompt for AI Assistant:

```
CONTEXT:
FortSight AI includes RAG chatbot that answers fort questions.
Can query static knowledge (history) or dynamic (current visibility).
Supports Marathi language.

TASK:
Implement RAG chatbot:

1. Document ingestion:
   scripts/ingest_documents.py:
   
   Sources:
   - Fort historical documents (Markdown)
   - Tourism information
   - User-curated docs
   - Wikipedia (with attribution)
   
   Process:
   - Parse document
   - Split into chunks (500-1000 tokens)
   - Generate embeddings (using Sentence Transformers)
   - Store in pgvector
   - Maintain source attribution
   - Support both English and Marathi

2. Vector database (pgvector):
   historical_documents table:
   - id
   - title
   - content (full text)
   - source_url
   - fort_id (optional)
   - language
   - created_at
   
   document_chunks table:
   - id
   - document_id
   - chunk_index
   - content (chunk text)
   - embedding (pgvector type, 384-dim)
   - created_at

3. Embedding model:
   - Use Sentence Transformers (multilingual)
   - Model: paraphrase-multilingual-MiniLM-L12-v2
   - Dimension: 384
   - Free to use, no API key needed
   - Can run locally

4. Query classification:
   app/services/query_classifier.py:
   
   Classify queries as:
   - STATIC_KNOWLEDGE: "Who built Rajgad?"
   - SPATIAL_QUERY: "What forts can I see from here?"
   - HYBRID_QUERY: "Which fort can I see and what's its history?"
   
   Methods:
   - Keyword matching
   - Semantic similarity
   - Simple rules

5. Retriever:
   app/services/rag_retriever.py:
   
   For STATIC_KNOWLEDGE:
   - Embed query
   - Search pgvector
   - Retrieve top-K similar chunks
   - Re-rank by relevance
   - Return with source attribution
   
   For SPATIAL_QUERY:
   - Call visibility API
   - Combine fort info
   - Return with live data
   
   For HYBRID_QUERY:
   - Get visible forts
   - Retrieve history for each
   - Combine results

6. LLM integration:
   app/services/llm_service.py:
   
   Use Claude/GPT API:
   - Flexible provider (not hardcoded)
   - Support for Marathi responses
   - With RAG context
   - Cite sources
   - Structured output
   
   Prompt template:
   """
   You are FortSight AI assistant, helping users explore Maharashtra forts.
   Be helpful, accurate, and friendly.
   Support Marathi language.
   Always cite your sources.
   
   Context:
   {context}
   
   User query: {query}
   User location (optional): {lat}, {lon}
   
   Respond in the user's language.
   Cite sources using [Source: document title].
   """

7. Chat API endpoint:
   POST /api/v1/chat
   
   Request:
   {
     "message": "मी इथून कोणता किल्ला पाहू शकतो?",
     "session_id": "...",
     "latitude": 18.67,
     "longitude": 73.33,
     "heading": 245
   }
   
   Response:
   {
     "message": "आपणांस इथून तोरणा, राजगड... दिसू शकतात",
     "sources": [
       { "title": "Torna Fort History", "url": "..." }
     ],
     "visible_forts": [
       { "name": "Torna", "distance": 12.4, ... }
     ],
     "session_id": "..."
   }

8. Session management:
   - Store conversation history
   - Per-user sessions
   - TTL for sessions (24 hours)
   - Support multiple conversations

9. Rate limiting:
   - Limit messages per session
   - Limit per IP address
   - LLM API call limiting
   - Clear error on limit exceeded

10. Caching:
    - Cache embeddings
    - Cache retrieved documents
    - Cache LLM responses for identical queries
    - Cache visibility results

11. Frontend:
    Components/ChatBot.tsx:
    - Chat interface (messages)
    - Input box
    - Send button
    - Show thinking/loading
    - Display sources
    - Show visible forts if mentioned
    - Copy message
    - Clear conversation
    - Voice input (optional future)

12. Error handling:
    - No LLM API key configured
    - LLM API timeout
    - No documents found
    - Invalid query
    - Rate limit exceeded
    - Graceful fallback responses

13. Testing:
    - Query classification tests
    - Retrieval tests
    - End-to-end chat tests
    - Multi-language tests

14. Documentation:
    - RAG architecture explanation
    - How to add documents
    - LLM provider setup
    - Marathi support details
    - Limitations

IMPORTANT:
- Use provider-agnostic LLM integration
- Cite sources always
- No hallucinations for spatial queries
- Support both English and Marathi
- Clear error messages
- Rate limiting
- Session management

OUTPUT:
1. Document ingestion script
2. pgvector setup
3. Embedding service
4. Query classifier
5. RAG retriever
6. LLM service (provider abstraction)
7. Chat API endpoint
8. Session management
9. Frontend ChatBot component
10. Tests (comprehensive)
11. Documentation
```

### Deliverables:
- Document ingestion pipeline
- pgvector embedding storage
- Query classifier
- RAG retriever
- LLM service with provider abstraction
- Chat API endpoint
- Frontend chat interface
- Session management
- Tests

### Verification:
```bash
# Ingest documents
python scripts/ingest_documents.py --source historical_docs

# Test chat endpoint
POST http://localhost:8000/api/v1/chat
{
  "message": "राजगडाचा इतिहास",
  "latitude": 18.67,
  "longitude": 73.33
}

# Should return:
# - Answer about Rajgad history
# - Source attribution
# - Marathi support
```

### When Complete: Proceed to Phase 13

---

## PHASE 13: Optional ML Components

### Goal
Implement optional ML features (not required for MVP).

### Prompt for AI Assistant:

```
CONTEXT:
Advanced optional features using machine learning.
Not required for MVP, but cool to add.

TASK:
Design (not fully implement) ML components:

1. Fort image recognition:
   Service: FortImageClassifier
   
   Feature:
   - User uploads photo of fort
   - Model predicts which fort (Rajgad / Torna / etc.)
   - Return confidence score
   - Suggest matching forts if uncertain
   
   Implementation:
   - Transfer learning on MobileNet/EfficientNet
   - Training: collection of fort photos
   - Input: 224x224 RGB image
   - Output: fort class + confidence
   - Threshold: >80% confidence to suggest
   
   Dataset: Collect fort photos
   Data augmentation: rotation, brightness, blur
   Training: 80/20 split
   Validation: precision, recall, F1, confusion matrix
   Deployment: TensorFlow Lite or ONNX for mobile

2. Visibility confidence prediction:
   Service: VisibilityConfidenceModel
   
   Feature:
   - Given visibility result, predict confidence
   - Factor in: DEM resolution, distance, terrain complexity
   - Return calibrated confidence
   
   Implementation:
   - Training data: known visibility cases + actual observations
   - Features: distance, terrain_ruggedness, dem_resolution, angle
   - Model: Random Forest or Gradient Boosting
   - Output: confidence 0-1

3. Trek difficulty prediction:
   Service: TrekDifficultyModel
   
   Feature:
   - Predict trek difficulty from trail characteristics
   - Input: elevation gain, distance, terrain type
   - Output: Easy / Medium / Hard
   
   Implementation:
   - Training data: curated trek database
   - Model: Classification (3 classes)
   - Explainability: show factors contributing to difficulty

4. Landmark recognition:
   Service: LandmarkRecognizer
   
   Feature:
   - User uploads photo of a landmark/structure
   - Model identifies structure type (gate, machi, temple, etc.)
   - Suggest fort location if possible
   
   Implementation:
   - Custom dataset of fort structures
   - Classification model
   - Localization (optional)

5. Implementation guidelines:
   - No ML model dependency for core visibility
   - Optional feature endpoints
   - Model serving strategy (TensorFlow Serving / ONNX Runtime)
   - Model versioning
   - A/B testing for model updates
   - Model monitoring (accuracy drift)
   - Fallback when model unavailable

6. Storage:
   - Model files in /models directory
   - Version tracking
   - Training/validation data (separate from repo)
   - Model performance metrics

7. Testing:
   - Unit tests for feature extraction
   - Integration tests for predictions
   - Performance benchmarks (inference time)

IMPORTANT:
- Do NOT implement full ML if not needed
- Create framework for future ML
- Document potential ML additions
- Maintain core functionality without ML
- Clear fallback mechanisms

OUTPUT:
1. ML service architecture
2. Feature engineering guide
3. Model serving setup
4. Placeholder model classes
5. Data collection strategy
6. Training pipeline outline
7. Integration points
8. Documentation
```

### Deliverables:
- ML service architecture
- Feature engineering templates
- Model serving setup
- Training pipeline outline
- Data collection strategy
- Integration documentation

### When Complete: Proceed to Phase 14

---

## PHASE 14: Testing & Quality Assurance

### Goal
Comprehensive test coverage across all components.

### Prompt for AI Assistant:

```
CONTEXT:
Implement testing for FortSight AI.
Backend: pytest, Frontend: Vitest + React Testing Library.

TASK:
Build complete test suite:

1. Backend tests (app/tests/):
   
   a. Unit tests:
      - test_distance_calculation.py
      - test_bearing_calculation.py
      - test_direction_conversion.py
      - test_elevation_queries.py
      - test_visibility_score.py
      - test_database_models.py
      - test_pydantic_schemas.py
   
   b. Integration tests:
      - test_visibility_api.py
      - test_fort_api.py
      - test_terrain_api.py
      - test_chat_api.py
      - test_database_migrations.py
   
   c. Performance tests:
      - test_visibility_performance.py
      - test_query_performance.py
      - test_caching_efficiency.py
   
   d. Edge cases:
      - Invalid coordinates
      - Out-of-bounds queries
      - Missing data
      - Concurrent requests

2. Frontend tests (frontend/src/__tests__/):
   
   a. Component tests:
      - Map.test.tsx
      - LocationPanel.test.tsx
      - FortList.test.tsx
      - ChatBot.test.tsx
   
   b. Hook tests:
      - useLocation.test.ts
      - useHeading.test.ts
      - useForts.test.ts
      - useVisibility.test.ts
   
   c. Utility tests:
      - bearingToDirection.test.ts
      - formatDistance.test.ts
   
   d. API service tests:
      - api.test.ts (mocked calls)

3. End-to-end tests:
   - User opens app
   - Grants permissions
   - Sees location and forts
   - Clicks fort
   - Sees details
   - Uses chatbot
   - etc.

4. Test data & fixtures:
   - Mock elevation data
   - Sample forts
   - Sample visibility results
   - Mock API responses
   - Test database seeding

5. CI/CD integration:
   - GitHub Actions
   - Run tests on PR
   - Code coverage reporting
   - Lint checks
   - Build verification

6. Coverage goals:
   - Backend: 80%+ coverage
   - Frontend: 70%+ coverage
   - Critical paths: 100%
   - Report coverage metrics

IMPORTANT:
- Test actual calculations
- Mock external dependencies
- Test error scenarios
- Load test visibility API
- Test on multiple devices/browsers

OUTPUT:
1. Complete test suite for backend
2. Complete test suite for frontend
3. Test fixtures and mocks
4. CI/CD configuration
5. Coverage reports
6. Testing guide
```

### Deliverables:
- Comprehensive backend test suite
- Frontend component + hook tests
- E2E test framework
- Mock data and fixtures
- CI/CD pipeline
- Coverage reports

### When Complete: Proceed to Phase 15

---

## PHASE 15: Docker Deployment & Documentation

### Goal
Production-ready deployment with comprehensive documentation.

### Prompt for AI Assistant:

```
CONTEXT:
FortSight AI ready for deployment.
Use Docker + Docker Compose.
Production-grade security and performance.

TASK:
Build deployment setup:

1. Production Docker configuration:
   - Multi-stage builds (optimize image size)
   - Frontend: Nginx serving React SPA
   - Backend: Gunicorn + FastAPI
   - PostgreSQL with persistent volumes
   - Redis for caching (optional)
   - Health checks for all services
   - Proper resource limits
   - Log aggregation

2. Security:
   - Environment secrets management
   - API key protection
   - CORS configuration
   - Rate limiting
   - Input validation
   - SQL injection prevention
   - No secrets in logs

3. Performance:
   - Frontend: CDN-ready
   - Backend: Async processing
   - Database: Optimized queries
   - Caching strategy
   - Compression (gzip)
   - Static file serving

4. Monitoring:
   - Application logs
   - Error tracking
   - Performance metrics
   - Uptime monitoring
   - Error alerts

5. Scaling:
   - Horizontal scalability
   - Load balancing (Nginx)
   - Database connection pooling
   - Cache layer

6. Documentation:
   a. README.md (complete)
   b. INSTALLATION.md
   c. DEPLOYMENT.md
   d. ARCHITECTURE.md
   e. API_REFERENCE.md
   f. CONTRIBUTING.md
   g. TROUBLESHOOTING.md
   h. FAQ.md
   i. PRIVACY.md
   j. LICENSE

7. Example deployments:
   - Single server deployment
   - Multi-container setup
   - Cloud deployment (AWS/GCP/Azure)
   - Kubernetes examples (optional)

IMPORTANT:
- Production-ready
- Security-first
- Easy to deploy
- Clear documentation
- Monitoring setup
- Backup strategy

OUTPUT:
1. Production docker-compose.yml
2. Nginx configuration
3. Gunicorn configuration
4. Environment templates
5. Deployment guide
6. Complete documentation
7. Monitoring setup
```

### Deliverables:
- Production Docker setup
- Nginx configuration
- Deployment guide
- Complete documentation (all guides)
- Monitoring configuration
- Backup/restore procedures

### When Complete:
**MVP IS COMPLETE & READY TO DEPLOY**

---

# Summary Table

| Phase | Goal | Duration | Key Output |
|-------|------|----------|-----------|
| 0 | Feasibility & Architecture | 1-2 days | Architecture diagram, risk register |
| 1 | Repository & Docker Setup | 1 day | Monorepo, Docker, dev environment |
| 2 | Database Schema | 1-2 days | PostGIS schema, models, migrations |
| 3 | Fort Data Ingestion | 1 day | Data pipeline, sample data |
| 4 | FastAPI Core | 1-2 days | App structure, endpoints |
| 5 | Terrain Engine | 2 days | DEM processing, elevation queries |
| 6 | Visibility Engine | 2-3 days | Core algorithm, line-of-sight |
| 7 | Visibility API | 1-2 days | REST endpoint, caching, optimization |
| 8 | React Frontend Base | 2 days | Map, components, styling |
| 9 | GPS & Orientation | 1-2 days | Location, heading, dev panel |
| 10 | Fort Details | 1-2 days | Details page, internal map |
| 11 | Fort Network | 1-2 days | Visibility graph, visualization |
| 12 | RAG Chatbot | 2-3 days | Document ingestion, chat API |
| 13 | Optional ML | 2-3 days | ML architecture, placeholder models |
| 14 | Testing | 2-3 days | Comprehensive test suite |
| 15 | Deployment | 1-2 days | Production setup, documentation |

**Total estimated time: 4-6 weeks** for a team, or **10-12 weeks** solo

---

# How to Use These Prompts

1. **Start with Phase 0**: Use the Phase 0 prompt to get architecture understanding
2. **For each phase**: Copy the prompt and give it to Claude/ChatGPT
3. **Follow exact structure**: Don't skip phases
4. **Test after each phase**: Verify deliverables before moving forward
5. **Adapt to your needs**: These are templates, customize as needed
6. **Document everything**: Keep notes as you progress

---

# Next Steps

1. Read Phase 0 prompt and run feasibility analysis
2. Confirm architecture approach
3. Get MVP scope agreement
4. Then proceed to Phase 1
5. Build incrementally
6. Test thoroughly

Good luck building FortSight AI! 🏰🗺️
