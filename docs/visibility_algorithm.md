# Visibility Engine Algorithm

The FortInsight Visibility Engine determines if a target fort is visible from an observer's location, considering geodesic distance, earth's curvature, atmospheric refraction, and terrain obstructions.

## Core Formula and Adjustments

### Distance and Bearing
- **Distance:** Calculated using the Haversine formula, providing the great-circle distance between two latitude/longitude points.
- **Bearing:** Initial bearing is calculated using `atan2` on the spherical projection coordinates.

### Curvature and Refraction
To accurately model line-of-sight over long distances, we must adjust for the curvature of the earth and the refraction of light through the atmosphere.
- **Earth Radius ($R$):** $6,371,000$ meters.
- **Refraction Coefficient ($k$):** $0.13$ (Standard atmospheric condition).
- **Effective Earth Radius ($R_e$):** $R_e = \frac{R}{1 - k} \approx 7,322,988$ meters.

**Elevation Adjustment Formula:**
The drop in elevation due to curvature at a distance $d$ from the observer is:
$$ \Delta h = \frac{d^2}{2 \cdot R_e} $$
This adjustment is applied to both the target elevation and the interpolated terrain elevations.

## Algorithm Steps

1. **Calculate Baseline Metrics:** Determine total geodesic distance and bearing between observer and target.
2. **Apply Initial Adjustments:** Compute total elevation for observer and target (base elevation + structure height). Adjust target elevation for curvature relative to the total distance.
3. **Calculate Line-of-Sight Slope:** Determine the viewing angle or slope from observer to target: `(Adjusted Target Z - Observer Z) / Total Distance`.
4. **Generate Sample Points:** Linearly interpolate points along the geodesic path. Sampling is adaptive, roughly 1 point every 100 meters.
5. **Analyze Terrain:**
   - For each intermediate point, retrieve terrain elevation using Bilinear Interpolation from the DEM Service.
   - Adjust terrain elevation for earth curvature based on the point's distance from the observer.
   - Calculate the Expected Line-of-Sight Elevation at that point: `Observer Z + (Slope * Distance)`.
   - Calculate Clearance: `Expected LOS Elevation - Adjusted Terrain Elevation`.
6. **Determine Status and Score:**
   - If Clearance < 0 at any point, the path is **BLOCKED**.
   - If Clearance >= 0 for all points, calculate a score based on the minimum clearance margin, the total distance (penalty for extreme distances), and observer height (slight bonus).
   - Score >= 0.9 = **VISIBLE**
   - Score 0.5 to 0.9 = **UNCERTAIN** (Usually due to very large distance or razor-thin clearance).
   - Score < 0.5 = **BLOCKED**

## Assumptions and Limitations
- **Atmospheric Conditions:** The $k=0.13$ constant assumes a standard atmosphere. Anomalous refraction (e.g., temperature inversions) can cause light to bend more or less, changing actual visibility.
- **Terrain Resolution:** Accuracy is bounded by the DEM resolution (e.g., 30m). Small obstructions like trees, buildings, or local boulders are not captured unless a high-resolution DSM is used.
- **Interpolation:** We use linear interpolation for intermediate coordinates, which approximates the great circle path well over distances typical for line-of-sight (up to 100km).
- **Performance:** Interpolating points and querying the DEM can be CPU-intensive. Caching DEM tiles and batched processing are essential for large-scale queries.

## Edge Cases Handled
- Target is in a deep valley: Will be correctly identified as blocked if surrounding terrain exceeds the sightline slope.
- Observer is very high up: Observer height is added directly to elevation, and a slight confidence bonus is given to the final score since a higher vantage point is generally more reliable.
- Edge of DEM: If a sample point falls outside the DEM bounds or on a NoData pixel, it is skipped. This is an assumption that missing data is "flat", though ideally, adjacent DEM tiles should be loaded.
