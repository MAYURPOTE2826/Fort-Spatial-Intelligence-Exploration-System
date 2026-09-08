# Troubleshooting Guide

## Docker Issues

### `docker-compose up` fails to start backend
- **Symptom:** Backend container exits immediately.
- **Solution:** Check the logs using `docker logs <backend-container-id>`. Ensure your `.env` file is present and has the correct `DATABASE_URL`. Check if `gunicorn_conf.py` has a syntax error.

### Postgres connection refused
- **Symptom:** `psycopg2.OperationalError: could not connect to server`.
- **Solution:** Ensure the database container is fully initialized. The `depends_on` block with `service_healthy` in `docker-compose.yml` usually handles this, but slow disks might cause timeouts. Restart the backend container.

## Application Issues

### Visibility Engine returns `0.0` always
- **Symptom:** Visibility scores are always zero or fail.
- **Solution:** Ensure the Digital Elevation Model (DEM) files (`.tif`) are correctly placed in the `data/dem/` directory and are mapped as volumes into the backend container if required, or ensure your automated download scripts ran properly.

### Nginx returns 502 Bad Gateway
- **Symptom:** Accessing the frontend yields a 502 error for API calls.
- **Solution:** The backend container might be down or not responding. Check backend logs. Also ensure the internal Docker networking allows Nginx to reach `http://backend:8000`.
