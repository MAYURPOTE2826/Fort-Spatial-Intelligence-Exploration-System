# PostGIS Index Strategy for FortSight AI

## Overview

A robust indexing strategy is essential to support complex geospatial queries, fast lookups, and TTL-based cache expirations in FortSight AI.

## 1. Spatial Indexes (GiST)
PostGIS spatial columns require GiST (Generalized Search Tree) indexes for bounding box and proximity calculations.

* **`forts.geometry`**: Essential for fast `ST_DWithin` and bounding box queries to locate forts in an area. GeoAlchemy2 automatically creates GiST indexes on `Geometry` columns by default.
* **`fort_viewpoints.geometry`**: Indexed for queries finding viewpoints within a fort's vicinity.
* **`fort_structures.geometry`**: Indexed for structural boundaries and point features.
* **`fort_trails.geometry`**: Indexed to quickly find nearby trails or intersect with user paths.
* **`terrain_tiles.geometry`**: Indexed to rapidly look up which elevation tile a specific Lat/Lon coordinate falls into.

## 2. Standard Lookups (B-Tree)
Standard B-Tree indexes will be applied on high-frequency lookup columns:

* **Primary Keys**: Automatically indexed by PostgreSQL.
* **Foreign Keys**: `fort_id` on viewpoints, structures, trails, and visibility tables are indexed to support fast joins and cascading deletes.
* **`users.email`**: Unique index for fast authentication lookups.
* **`forts.name`**: B-Tree index for quick autocomplete/search by name.
* **`terrain_tiles.tile_name`**: Unique index.

## 3. Visibility Cache (TTL Indexing)
The `visibility_results` table acts as a cache for computationally expensive Line-of-Sight calculations.

* **Composite Index / `expires_at`**: 
  - `expires_at` is indexed via B-Tree for fast cleanup of stale cache data (e.g., using a cron job `DELETE FROM visibility_results WHERE expires_at < NOW()`).
  - Indexing `observer_lat` and `observer_lon` (or combining them into a spatial point if desired) helps retrieve cached results near a user.

## 4. Document Search
For the `document_chunks` table used in the RAG architecture:

* **Vector Index (HNSW or IVFFlat)**: If migrating to `pgvector`, an HNSW index on the `embedding` column is highly recommended for low-latency nearest neighbor search (`<=>` or `<->` operators).
* **B-Tree**: Index on `document_id` for quick cascading retrieval.
