# Deployment Guide

This guide describes how to deploy FortSight AI in a production environment.

## Prerequisites

- A server (AWS EC2, DigitalOcean Droplet, GCP Compute Engine, etc.)
- **Docker** and **Docker Compose** installed on the server.
- A domain name (optional, but recommended).

## Single Server Deployment (Docker Compose)

The easiest way to deploy is using the provided `docker-compose.yml`. This setups the frontend (Nginx), backend (FastAPI/Gunicorn), Database (Postgres+pgvector), and Redis.

### 1. Prepare the Server

1. SSH into your production server.
2. Clone the repository:
   ```bash
   git clone https://github.com/MAYURPOTE2826/Fort-Spatial-Intelligence-Exploration-System.git
   cd Fort-Spatial-Intelligence-Exploration-System
   ```

### 2. Configure Secrets

1. Copy the production environment template:
   ```bash
   cp .env.production.example .env
   ```
2. Edit `.env` to include your secure secrets, database passwords, and API keys.

### 3. Build and Run

1. Build the multi-stage Docker images:
   ```bash
   docker-compose build
   ```
2. Start the services in detached mode:
   ```bash
   docker-compose up -d
   ```

### 4. Verify

Check the logs to ensure everything is running smoothly:
```bash
docker-compose logs -f
```
The application is now accessible via `http://<your-server-ip>` or `http://<your-domain>`.

## Cloud Native Deployments (AWS/GCP/Kubernetes)

For horizontal scalability, consider deploying the frontend via a CDN (like AWS CloudFront or Vercel) and the backend on managed container services (like AWS ECS, Google Cloud Run, or Kubernetes).

**Steps for Kubernetes:**
1. Build and push the Docker images to a container registry (e.g., Docker Hub, ECR).
2. Create standard Kubernetes Deployment and Service definitions for the backend and frontend.
3. Use a managed Postgres service (AWS RDS, Google Cloud SQL) with `pgvector` enabled, rather than a containerized database.

## Monitoring & Backups

### Monitoring Setup
- **Logs:** Docker Compose uses the `json-file` driver. You can hook this into ELK (Elasticsearch, Logstash, Kibana) or Datadog using Docker log drivers.
- **Health Checks:** The `docker-compose.yml` natively implements health checks that restart unhealthy containers.

### Backups
Schedule daily Postgres dumps to an S3 bucket:
```bash
docker exec -t [db_container_name] pg_dumpall -c -U postgres > dump_`date +%d-%m-%Y"_"%H_%M_%S`.sql
```
