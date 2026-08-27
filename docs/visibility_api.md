# Visibility REST API Documentation

## Base URL
`/api/v1/visibility`

---

## 1. Get Visibility From Location

**Endpoint:** `GET /from-location`

Calculates which forts are visible from a specific coordinate.

**Query Parameters:**
- `lat` (float, required): Observer latitude (-90 to 90)
- `lon` (float, required): Observer longitude (-180 to 180)
- `heading` (float, optional): Compass heading in degrees (0-360)
- `fov` (float, optional): Field of view in degrees (default: 60)
- `radius_km` (float, optional): Search radius (default: 50, max: 200)
- `elevation` (float, optional): Observer elevation in meters. If omitted, will be queried from DEM.
- `observer_height` (float, optional): Height of observer's eyes above ground in meters (default: 1.7)

**Rate Limit:** 10 requests per minute per IP

---

## 2. Get Visibility Between Forts

**Endpoint:** `POST /between-forts`

Checks if target fort is visible from source fort.

**Request Body (JSON):**
```json
{
  "source_fort_id": "string",
  "target_fort_id": "string"
}
```

**Rate Limit:** 20 requests per minute per IP

---

## 3. Build Visibility Network

**Endpoint:** `POST /build-network`

Generates a visibility graph/network among a list of forts.

**Request Body (JSON):**
```json
{
  "fort_ids": ["fort1", "fort2", "fort3"]
}
```

**Rate Limit:** 2 requests per minute per IP
