# FortSight AI — Production Audit

> **Audit Date:** 2026-09-09  
> **Auditor:** Senior Software Architect (Automated Inspection)  
> **Repository:** `d:\FortInsight`  
> **Commit state:** current working tree  

---

## 1. Architecture Overview

### 1.1 Current Architecture Diagram

```
Internet
    ↓
[Nginx] (port 80) — frontend/nginx.conf
    ↓
[React + TypeScript + Vite] (static SPA)
    ↓ (REST API calls to /api/v1)
[FastAPI + Gunicorn + Uvicorn workers] (port 8000)
    ↓
[PostgreSQL 15 + PostGIS + pgvector] (port 5432)
[Redis 7] (port 6379) ← declared in docker-compose but NOT actually used
```

**Docker services:** `frontend`, `backend`, `db` (ankane/pgvector:v0.5.1), `redis`

### 1.2 Frontend Architecture

- **Framework:** React 18 + TypeScript + Vite 5
- **Styling:** TailwindCSS 3 (configured with custom `terrain-*` color palette)
- **Map:** React-Leaflet 4 with OpenStreetMap tiles
- **State:** TanStack Query v5 (server state), local `useState` (UI state)
- **Routing:** React Router v7
- **Network Graph:** react-force-graph-2d
- **Icons:** Lucide React

**Pages (3 total):**
1. `MapPage` — Main map view, location + heading + visibility + fort list + chatbot
2. `FortDetailsPage` — Tabbed detail view (overview, map, viewpoints, trails, gallery, related)
3. `NetworkPage` — Fort-to-fort visibility network graph

**Components (16 total):**
`ChatBot`, `DevLocationPanel`, `FortGallery`, `FortHistory`, `FortList`, `FortMap`, `LocationPanel`, `Map`, `NetworkFilters`, `NetworkStats`, `PermissionDialog`, `RelatedForts`, `StructureInfo`, `TrailsList`, `ViewpointsList`, `VisibilityGraph`

**Hooks (4):** `useForts`, `useHeading`, `useLocation`, `useVisibility`

### 1.3 Backend Architecture

- **Framework:** FastAPI (async-capable but largely sync handlers)
- **WSGI/ASGI:** Gunicorn with Uvicorn workers (via `gunicorn_conf.py`)
- **ORM:** SQLAlchemy 2 (sync sessions)
- **Migrations:** Alembic (2 migrations: initial schema + terrain source column)
- **Rate limiting:** SlowAPI (IP-based)
- **Authentication:** python-jose JWT + passlib bcrypt (configured but NOT implemented)
- **Request IDs:** UUID per request via middleware

**API v1 Endpoints:**

| Route | Handler | Status |
|---|---|---|
| `GET /health` | health_check | Functional |
| `GET /ready` | readiness_check | Stubbed (no DB check) |
| `POST /auth/login` | login | **MOCK — returns dummy_token** |
| `POST /auth/register` | register | **STUB — unimplemented** |
| `GET /forts/` | get_forts | **MOCK — hardcoded Python dict** |
| `GET /forts/{id}` | get_fort | **MOCK — hardcoded Python dict** |
| `GET /forts/{id}/structures` | get_fort_structures | **MOCK** |
| `GET /forts/{id}/viewpoints` | get_fort_viewpoints | **MOCK** |
| `GET /forts/{id}/trails` | get_fort_trails | **MOCK** |
| `GET /forts/{id}/connections` | get_fort_connections | **MOCK** |
| `GET /visibility/from-location` | get_visibility_from_location | Functional (requires DEM + DB) |
| `POST /visibility/between-forts` | get_visibility_between_forts | Functional (requires DEM + DB) |
| `POST /visibility/build-network` | build_visibility_network | Functional |
| `GET /visibility/job/{id}` | get_job_status | Functional |
| `GET /terrain/elevation` | — | **STUB** |
| `GET /routes/` | get_routes | **STUB — returns empty list** |
| `GET /routes/{id}` | get_route | **STUB — returns "Dummy Route"** |
| `POST /chat/` | chat_query | Partially functional (requires GEMINI_API_KEY + embeddings) |
| `POST /ml/recognize-fort` | recognize_fort | Unknown (depends on ML stubs) |
| `POST /ml/visibility-confidence` | get_visibility_confidence | Unknown |
| `POST /ml/trek-difficulty` | get_trek_difficulty | Unknown |
| `POST /ml/recognize-landmark` | recognize_landmark | Unknown |

### 1.4 Database Architecture

**Tables (12):**

| Table | Purpose | Notes |
|---|---|---|
| `users` | Auth users | No `hashed_password` column — **auth cannot work** |
| `forts` | Fort records | Missing many fields (aliases, taluka, region, source_url, etc.) |
| `fort_viewpoints` | Viewpoint geometry | OK |
| `fort_structures` | Internal structures | OK |
| `fort_trails` | Trail linestrings | OK |
| `fort_connections` | Fort-to-fort visibility links | OK |
| `terrain_tiles` | DEM file registry | Missing `source` column in model vs migration schema |
| `historical_documents` | RAG source documents | Missing `language` column in migration |
| `document_chunks` | RAG chunks + vectors | Migration uses `ARRAY(Float)` but model uses `pgvector.Vector(384)` — **schema mismatch** |
| `chat_sessions` | Chat sessions | Migration uses `Integer` PK but model uses `String` (UUID) — **schema mismatch** |
| `chat_messages` | Chat messages | OK |
| `visibility_results` | Cached results | OK |
| `visibility_cache` | Key-value cache | **NOT in migration** — only in model |

**Critical Schema Issues:**
1. `document_chunks.embedding`: Migration creates `ARRAY(Float)`, model uses `pgvector.Vector(384)` — pgvector queries will fail
2. `chat_sessions.id`: Migration creates `Integer`, model uses `String` — session creation will fail
3. `users` table has no `hashed_password` column — login/register cannot work
4. `visibility_cache` table is NOT in migration `001` — only auto-created via `Base.metadata.create_all()` at startup
5. `forts` table uses `geometry` column name but `crud.py` queries `location` column — **spatial queries broken**

### 1.5 GIS Architecture

- **DEM Provider:** Copernicus DEM 30m (COG TIF) via S3 URL
- **DEM Processor:** `DEMProcessor` — bilinear interpolation, lru_cache for file handles
- **Visibility Engine:** `calculate_line_of_sight()` — haversine, bearing, curvature + refraction correction, sample-based LOS
- **Coordinate system:** WGS84 (SRID 4326) throughout
- **Interpolation:** Linear between WGS84 lat/lon — NOT geodesic on sphere
- **Sampling:** Every ~100m along straight interpolated line

**Critical GIS Issues:**
1. `interpolate_points()` uses linear lat/lon interpolation — introduces error for long paths (should use geodesic)
2. DEM file path is hardcoded S3 URL in `visibility_service.py` (line 90) — different from config value
3. `crud.py` queries `location` and `base_elevation` columns but model defines `geometry` and `elevation` — **column name mismatch**
4. `dem_processor.get_elevation()` called with hardcoded S3 URL in `visibility_service.py` — will fail without `rasterio` S3 support or local file
5. No DEM file bundled — S3 requires AWS credentials or public access

### 1.6 Data Pipeline

**Current state:**
- `data/forts.json` — 10 forts (name, lat, lon, base_elevation only)
- `data/forts_mvp.csv` — 10 forts (more fields including source="Wikipedia", image URLs are `example.com` placeholders)
- `data/forts_mvp.geojson` — GeoJSON of same 10 forts
- `data/trails.csv` — Trail records (unknown status)
- `data/viewpoints.csv` — Viewpoint records (unknown status)
- `data/documents/` — Historical documents (unknown contents)
- **No import scripts that actually load CSV → PostgreSQL**

### 1.7 AI/RAG Architecture

- **Embedding Model:** `paraphrase-multilingual-MiniLM-L12-v2` (sentence-transformers) — lazy-loaded, 384-dim
- **Vector Store:** pgvector (in PostgreSQL) — but schema mismatch means queries likely fail
- **LLM:** Google Gemini 2.5 Flash via `google-genai` SDK
- **Query Classification:** Keyword-based (spatial vs. static vs. hybrid) — very simple, no ML
- **Retrieval:** L2 distance search over `document_chunks`
- **Hybrid:** spatial retrieval + static retrieval combined in context

**Critical RAG Issues:**
1. `rag_retriever.retrieve_spatial()` calls `visibility_service.calculate_visibility(db, lat, lon)` — this method doesn't exist (the actual method is `calculate_visibility_from_location`)
2. pgvector schema mismatch means embedding queries will fail
3. No documents seeded — RAG will return empty context
4. GEMINI_API_KEY in `.env` file is likely a placeholder

### 1.8 Deployment Architecture

- **Production:** Docker Compose with Nginx + FastAPI + PostgreSQL + Redis
- **Frontend:** Nginx serving static Vite build
- **Backend:** Gunicorn + Uvicorn workers
- **DB:** ankane/pgvector:v0.5.1 image
- **Redis:** Declared but **NOT used in code** (rate limiter uses in-memory, cache uses PostgreSQL)

---

## 2. Current Feature Status

| Feature | Status | Quality | Problems | Priority |
|---|---|---|---|---|
| **Map** | PARTIAL | 4/10 | OpenStreetMap only, no terrain/satellite layers, no clustering, no layer control | P0 |
| **GPS** | PARTIAL | 6/10 | Browser Geolocation API works, no accuracy indicator on map | P1 |
| **Compass/Heading** | PARTIAL | 5/10 | DeviceOrientationEvent wired, permission dialog exists, sensor noise not smoothed | P1 |
| **Visibility Engine** | PARTIAL | 5/10 | Core algorithm exists but DEM path hardcoded, no DEM file bundled, column name mismatch in DB | P0 |
| **Terrain/DEM** | PARTIAL | 3/10 | DEMProcessor implemented but DEM not bundled, S3 path hardcoded, terrain API endpoint stubbed | P0 |
| **Fort Data** | MOCK | 2/10 | All fort API endpoints return hardcoded Python dicts for fort 1 (Sinhagad only), others return generic mock | P0 |
| **Fort Details** | PARTIAL | 4/10 | UI works for mock data; structures/viewpoints/trails all mock | P1 |
| **Fort Discovery** | MISSING | 0/10 | No search, no filter, no sort beyond distance | P0 |
| **Trails** | MOCK | 2/10 | Mock trail for fort 1 only, routes API returns empty list | P1 |
| **Network** | PARTIAL | 5/10 | Network graph UI works, visibility calculation engine works, but requires DEM + DB data | P1 |
| **RAG Chatbot** | PARTIAL | 3/10 | Chat endpoint wired, but `retrieve_spatial` calls wrong method, no documents seeded, pgvector schema broken | P1 |
| **Authentication** | BROKEN | 0/10 | Login returns dummy token, register returns "not implemented", no password column in DB | P0 |
| **User Accounts** | MISSING | 0/10 | No favorites, no saved routes, no profile page | P2 |
| **Trek Planner** | MISSING | 0/10 | Routes endpoint returns empty list | P2 |
| **PWA/Offline** | MISSING | 0/10 | No service worker, no manifest | P2 |
| **Internationalization** | PARTIAL | 3/10 | Marathi fort names stored, query classifier has some Marathi keywords, no i18n framework | P2 |
| **Weather** | MISSING | 0/10 | Not implemented | P3 |
| **Admin Panel** | MISSING | 0/10 | No admin routes, no RBAC | P2 |
| **Testing** | PARTIAL | 4/10 | GIS unit tests good; unit test for visibility service tests non-existent interface; conftest uses SQLite (incompatible with PostGIS) | P1 |
| **CI/CD** | PARTIAL | 5/10 | GitHub Actions exist for lint + test + build but will fail due to bugs | P1 |
| **Deployment** | PARTIAL | 6/10 | Docker Compose configured, Nginx configured, health checks exist | P1 |
| **Observability** | PARTIAL | 4/10 | Request logging + timing exists, no metrics endpoint, no structured JSON logs | P2 |
| **Security** | BROKEN | 2/10 | Hardcoded secret key, no auth working, password exposed in .env | P0 |

---

## 3. Technical Debt

### 3.1 Critical Bugs (Breaks Core Functionality)

#### BUG-001: Column Name Mismatch — `crud.py` vs `forts` model
**File:** `backend/app/crud.py`  
**Problem:** `crud.py` queries `location` and `base_elevation` columns, but the `Fort` model and migration define them as `geometry` and `elevation`. Every PostGIS spatial query in the visibility service will throw a `psycopg2.errors.UndefinedColumn` exception.  
**Impact:** Visibility calculation from location completely broken.

#### BUG-002: `chat_sessions` Primary Key Type Mismatch
**File:** `backend/alembic/versions/001_initial_schema.py` vs `backend/app/models/rag.py`  
**Problem:** Migration creates `chat_sessions.id` as `Integer`. Model defines it as `String` (UUID). `db.add(ChatSession(id=session_id))` where `session_id` is a UUID string will fail with a type error.  
**Impact:** All chat sessions fail to create.

#### BUG-003: `document_chunks.embedding` Type Mismatch
**File:** `backend/alembic/versions/001_initial_schema.py` vs `backend/app/models/rag.py`  
**Problem:** Migration creates column as `ARRAY(Float)`, model uses `pgvector.Vector(384)`. The `l2_distance` pgvector operator won't work on `ARRAY(Float)`.  
**Impact:** All RAG retrieval queries fail.

#### BUG-004: `rag_retriever` Calls Non-Existent Method
**File:** `backend/app/services/rag_retriever.py:39`  
**Problem:** `visibility_service.calculate_visibility(db, lat, lon)` does not exist. The actual method is `VisibilityService.calculate_visibility_from_location(db, lat, lon, heading, fov, radius_km, elevation, observer_height)`.  
**Impact:** All spatial RAG queries crash.

#### BUG-005: `users` Table Missing `hashed_password`
**File:** `backend/app/models/users.py` + migration  
**Problem:** No `hashed_password` column exists. Auth endpoint returns dummy token without any user lookup.  
**Impact:** Authentication completely broken.

#### BUG-006: `visibility_cache` Table Not in Migration
**File:** `backend/app/models/visibility.py` vs migrations  
**Problem:** `VisibilityQueryCache` model exists but is not in Alembic migration. It's created only by `Base.metadata.create_all()` (startup). If Alembic is used exclusively (as it should be in production), this table won't exist.  
**Impact:** Visibility caching broken in proper Alembic-managed deployments.

#### BUG-007: DEM Path Hardcoded in Two Locations
**Files:** `backend/app/services/visibility_service.py:90`, `backend/app/gis/visibility_engine.py:76`  
**Problem:** S3 path `s3://copernicus-dem-30m/...` hardcoded. `DEMProcessor.get_elevation` calls `rasterio.open(file_path)` which won't work for S3 without `rasterio[s3]` or explicit GDAL config. `dem_processor.get_elevation` in `visibility_service.py` still uses this S3 URL when elevation is None.  
**Impact:** Observer elevation lookup fails without a local DEM file.

#### BUG-008: `terrain_service.py` References Undefined Variable
**File:** `backend/app/services/terrain_service.py:20`  
**Problem:** `elevation_cache` dict is referenced but never defined in the service. `@lru_cache` is applied to a static method with a `db: Session` argument — unhashable/non-comparable, will cause `TypeError`.  
**Impact:** Terrain service crashes on any call.

#### BUG-009: `forts` API Returns Only Mock Data
**File:** `backend/app/api/v1/endpoints/forts.py`  
**Problem:** Entire endpoint file uses hardcoded `MOCK_FORTS_DETAILS`, `MOCK_STRUCTURES`, etc. No database queries at all. Only Sinhagad (fort 1) has details; all others return a generic fallback.  
**Impact:** Fort discovery, details, trails, viewpoints, connections all return fake data.

#### BUG-010: `test_visibility_service.py` Tests Wrong Interface
**File:** `backend/tests/unit/test_visibility_service.py`  
**Problem:** Tests mock `terrain_service.get_elevation`, `fort_service.get_forts_in_radius`, and `los_engine.calculate_los` — none of which exist in the current implementation. Test will fail with `ModuleNotFoundError` or `AttributeError`.  
**Impact:** Backend unit test suite is broken.

### 3.2 Security Issues

| Issue | Severity | File |
|---|---|---|
| Hardcoded `SECRET_KEY` in config.py (default value) | CRITICAL | `backend/app/core/config.py:20` |
| Real `POSTGRES_PASSWORD` and `GEMINI_API_KEY` in `.env` file (should not be committed) | HIGH | `.env` |
| Auth endpoint returns dummy JWT token without verification | CRITICAL | `backend/app/api/v1/endpoints/auth.py` |
| No CSRF protection | MEDIUM | All state-changing endpoints |
| No input sanitization on chat message | MEDIUM | `backend/app/api/v1/endpoints/chat.py` |
| `/ready` endpoint has TODO for DB check — no real readiness signal | LOW | `backend/app/api/v1/endpoints/health.py` |
| CORS allows localhost only — OK for dev but needs production config | LOW | `backend/app/core/config.py:25` |
| Redis declared but not used — rate limiter state is in-memory (resets on restart) | MEDIUM | `backend/app/core/rate_limit.py` |

### 3.3 Duplicated / Stale Code

- `backend/app/services/chat_service.py` — empty stub (`ChatService.get_chat_response` is `pass`), not imported anywhere
- `backend/app/services/fort_service.py` — empty stub, not imported anywhere (unit test imports it incorrectly)
- `backend/app/los_engine.py` — appears to exist at the top `app/` level and also test imports it, but no such file found — unclear if this is a leftover or never created
- `backend/app/test_dem.py` — test file inside app source directory (should be in `tests/`)
- `backend/import_trace.log` — 276KB import trace log committed to repo
- `backend/install_log.txt`, `backend/install_output.txt`, `backend/uvicorn_test.log` — debug logs committed to repo

### 3.4 Hardcoded Values

| Value | Location | Impact |
|---|---|---|
| S3 DEM URL | `visibility_service.py:90`, `visibility_engine.py:76` | DEM lookup broken |
| `1.7` (observer height) | `visibility_service.py:200` | Should be configurable |
| `10.0` (target height assumption) | `visibility_service.py:125` | Poorly documented assumption |
| `200` km radius in `calculate_visibility_between_forts` | `visibility_service.py:198` | Huge search space |
| `100m` sampling interval | `visibility_engine.py:101` | Should be configurable based on distance |
| Mock fort data (entire `forts.py` endpoint) | `api/v1/endpoints/forts.py` | No database integration |

### 3.5 Missing Indexes

| Table | Column | Reason |
|---|---|---|
| `forts` | `geometry` | PostGIS spatial index (GiST) required for ST_DWithin |
| `forts` | `difficulty`, `district` | For filter queries |
| `fort_trails` | `fort_id` | Missing index on FK |
| `fort_structures` | `fort_id` | Missing index on FK |
| `document_chunks` | `embedding` (IVFFlat/HNSW) | pgvector ANN index required for performance |
| `visibility_cache` | `expires_at` | For cache eviction queries |
| `chat_sessions` | `user_id` | Missing index on FK |

**Note:** GeoAlchemy2 creates a GiST index on geometry columns by default on `create_all()` but the migration does NOT include explicit spatial index creation.

### 3.6 Performance Issues

1. **Synchronous visibility calculations** — LOS runs in `ThreadPoolExecutor` but each thread calls `dem_processor.get_elevation` which does file I/O. With S3, latency would be enormous.
2. **No Redis cache** — Visibility query cache stored in PostgreSQL (slow). Redis is declared but unused.
3. **`@lru_cache` on static method with `db: Session`** — Incorrect; Session is unhashable.
4. **`interpolate_points` uses linear interpolation** — Not geodesically accurate for distances > 20km.
5. **Network job stores progress in `VisibilityQueryCache`** — Mixes progress tracking with result caching.
6. **`sentence-transformers` model loaded at import time** — Adds startup latency if model isn't cached.
7. **fort details page makes 5 parallel API calls**, all returning mock data.

### 3.7 UX Problems

1. No loading skeletons (just text "Loading Tactical Data...")
2. No empty states (fort list shows nothing when no forts loaded)
3. No error states with actionable guidance
4. Fort list on mobile limited to 40vh but not clearly communicating scroll
5. "FortSight" branding only visible as small text; no proper landing page
6. No offline indicator
7. `DevLocationPanel` appears in production (`import.meta.env.DEV || false`)
8. Map has only OSM tiles — no terrain, satellite, or dark map options
9. Fort markers not clustered — will be unusable with 100+ forts
10. Tab navigation in `FortDetailsPage` uses text "Tactical Data" loading message instead of skeleton
11. Missing `<title>` and `<meta>` tags per page
12. No toast notifications or success feedback

---

## 4. Production Readiness Score

| Dimension | Score | Key Failures |
|---|---|---|
| **Architecture** | 6/10 | Schema mismatches, Redis unused, DEM not bundled |
| **Backend** | 3/10 | Forts API entirely mock, auth broken, terrain service broken, test interface wrong |
| **Frontend** | 5/10 | Works for display but tied to mock data, no i18n, poor mobile UX |
| **GIS** | 4/10 | LOS engine algorithmically sound but DEM inaccessible, column name wrong |
| **Data Quality** | 1/10 | 10 forts, placeholder image URLs, no trail geometry, no historical docs seeded |
| **AI/RAG** | 2/10 | Three critical bugs, no documents, wrong method call |
| **Security** | 1/10 | Hardcoded secret, dummy auth token, no real auth |
| **Performance** | 4/10 | ThreadPool for LOS is good; Redis unused; no DB indexes documented |
| **Testing** | 3/10 | GIS tests good; service-layer tests broken; no integration tests |
| **DevOps** | 5/10 | Docker/CI exists but will fail to build without DEM; CI would fail tests |
| **UX** | 4/10 | Functional look but missing loading/empty/error states, mobile issues |

**Overall Production Readiness:** **3.5 / 10**

---

## 5. Prioritized Improvement Plan

### P0 — Must Fix (Blockers)

| ID | Issue | Effort | Impact |
|---|---|---|---|
| P0-001 | Fix `forts` DB column names in `crud.py` (`geometry`/`elevation`) | XS | Unblocks visibility |
| P0-002 | Fix `chat_sessions.id` type in migration (Integer → String) | S | Unblocks chat |
| P0-003 | Fix `document_chunks.embedding` type in migration (ARRAY → vector) | S | Unblocks RAG |
| P0-004 | Add `hashed_password` to `users` model + migration | S | Unblocks auth |
| P0-005 | Add `visibility_cache` to migration | XS | Unblocks caching |
| P0-006 | Fix `rag_retriever` spatial method call | XS | Unblocks spatial chat |
| P0-007 | Fix `terrain_service.py` (remove `lru_cache` misuse, define cache dict) | S | Unblocks terrain API |
| P0-008 | Implement `forts.py` endpoint with real DB queries | M | Unblocks all fort features |
| P0-009 | Create fort data seeding script (load `forts_mvp.csv` into DB) | M | Actual fort data in DB |
| P0-010 | Add PostGIS spatial index (GiST) to migrations | S | Required for ST_DWithin performance |
| P0-011 | Bundle or configure local DEM file + fix hardcoded S3 URLs | M | Unblocks visibility engine |
| P0-012 | Add `SPATIAL_INDEX` on `forts.geometry` to migration | XS | Performance |

### P1 — High Value

| ID | Issue | Effort | Impact |
|---|---|---|---|
| P1-001 | Implement proper JWT authentication (register + login + protected routes) | L | Security + user features |
| P1-002 | Implement terrain profile API (for visibility explanation) | M | Core feature |
| P1-003 | Fix and expand test suite (service layer mocks corrected) | M | Engineering quality |
| P1-004 | Wire up Redis for rate limiting + visibility cache | M | Performance |
| P1-005 | Add fort search/filter/sort to API + frontend | L | Discovery feature |
| P1-006 | Create RAG document ingestion script | M | Chatbot actually useful |
| P1-007 | Implement fort details from DB (remove all mock data) | M | Real fort information |
| P1-008 | Add map layers (terrain, satellite, dark) | S | Map UX |
| P1-009 | Add marker clustering | S | Map scalability |
| P1-010 | Add loading skeletons + empty states + error states | M | UX polish |
| P1-011 | Add PostGIS IVFFlat/HNSW index to `document_chunks.embedding` | XS | RAG performance |
| P1-012 | Document visibility methodology properly | M | Scientific credibility |

### P2 — Nice to Have

| ID | Issue | Effort | Impact |
|---|---|---|---|
| P2-001 | PWA (manifest + service worker + offline) | L | Mobile trekker value |
| P2-002 | Trek planner feature | XL | New feature |
| P2-003 | User favorites + saved routes | L | Engagement |
| P2-004 | Admin panel + data health dashboard | XL | Maintainability |
| P2-005 | Full internationalization (i18n) | L | Marathi users |
| P2-006 | Weather provider abstraction | M | Contextual info |
| P2-007 | Analytics dashboard | L | Product insights |
| P2-008 | SEO + OpenGraph metadata | S | Discoverability |
| P2-009 | Shareable links | S | Social sharing |
| P2-010 | Terrain profile visualization (chart) | M | Key demo feature |

---

## 6. Files to Clean Up

The following files should be removed from the repository:
- `backend/import_trace.log` (276KB)
- `backend/install_log.txt`
- `backend/install_output.txt`
- `backend/uvicorn_test.log`
- `backend/app/test_dem.py` (move to `tests/`)

`.env` should be gitignored and not contain real credentials.

---

*End of audit. See `docs/DATA_QUALITY.md` for data quality analysis and `docs/VISIBILITY_METHODOLOGY.md` for visibility algorithm details.*
