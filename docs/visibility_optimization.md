# Visibility Performance Optimization

1. **Spatial Filtering**:
   We use PostGIS `ST_DWithin` to aggressively filter forts within the `radius_km`. This runs in milliseconds using GiST indexes on geography columns.

2. **Concurrency**:
   LOS calculations for multiple forts are executed concurrently using Python's `concurrent.futures.ThreadPoolExecutor`. Because reading from the DEM via `rasterio` may involve I/O, threads provide a significant speedup over sequential execution.

3. **Rate Limiting**:
   Using `slowapi`, requests are limited per IP to prevent DoS attacks. Network building endpoints have stricter rate limits due to `N x (N-1)` complexity.

4. **Response Caching**:
   Complete JSON responses are cached in PostgreSQL. A cache hit bypasses all calculations and PostGIS lookups, resulting in sub-10ms response times.
