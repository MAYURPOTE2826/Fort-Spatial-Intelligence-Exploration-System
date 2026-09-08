# API Reference

This document outlines the core RESTful endpoints provided by the FortSight AI backend. A complete OpenAPI specification is available by navigating to `/docs` on the running application.

## 1. Forts API

### `GET /api/v1/forts/`
Retrieves a list of all forts.
- **Response:** `200 OK` (Array of Fort Objects)

### `GET /api/v1/forts/{id}`
Retrieves detailed information about a specific fort.
- **Parameters:** `id` (integer)
- **Response:** `200 OK` (Fort Object) or `404 Not Found`

## 2. Visibility API

### `POST /api/v1/visibility/calculate`
Calculates the line of sight and visibility score between two geographic coordinates.
- **Body:**
  ```json
  {
    "observer_lat": 18.234,
    "observer_lon": 73.567,
    "target_lat": 18.456,
    "target_lon": 73.890,
    "observer_height": 1.7,
    "target_height": 10.0
  }
  ```
- **Response:** `200 OK`
  ```json
  {
    "visibility_status": "VISIBLE",
    "visibility_score": 0.95,
    "distance": 25000,
    "elevation_profile": [...]
  }
  ```

## 3. Chat API

### `POST /api/v1/chat/`
Submits a query to the RAG chatbot for Marathi-aware Fort intelligence.
- **Body:**
  ```json
  {
    "message": "Tell me about the history of Rajgad",
    "history": []
  }
  ```
- **Response:** `200 OK`
  ```json
  {
    "response": "Rajgad was the first capital of the Maratha Empire...",
    "sources": [...]
  }
  ```
