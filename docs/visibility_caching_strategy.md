# Visibility Caching Strategy

The Visibility Engine relies on computationally heavy Line-of-Sight (LOS) calculations over Digital Elevation Model (DEM) data.

## Cache Key
Cache keys are deterministically generated using an MD5 hash of the request parameters.
Float parameters (lat, lon) are rounded to 4 decimal places (~10m precision) to maximize cache hits while maintaining spatial relevance.

## Storage
The cache is stored in PostgreSQL using the `visibility_cache` table.
- `cache_key`: MD5 hash string (Primary Key)
- `response_payload`: JSON string of the entire API response (for O(1) serialization)
- `created_at`: Timestamp
- `expires_at`: Timestamp (Default 24 hour TTL)

## Eviction & Invalidations
- The cache uses TTL-based eviction.
- Cron jobs or application logic should delete rows where `expires_at < NOW()`.
- If underlying DEM data or fort data is updated, the entire `visibility_cache` table can be truncated.
