.PHONY: up down build logs test shell-backend shell-frontend db-shell clean

# Start the development environment
up:
	docker-compose up -d

# Stop the development environment
down:
	docker-compose down

# Rebuild containers
build:
	docker-compose up -d --build

# View logs for all services
logs:
	docker-compose logs -f

# View backend logs
logs-backend:
	docker-compose logs -f backend

# View frontend logs
logs-frontend:
	docker-compose logs -f frontend

# Access backend shell
shell-backend:
	docker-compose exec backend /bin/bash

# Access frontend shell
shell-frontend:
	docker-compose exec frontend /bin/sh

# Access database shell
db-shell:
	docker-compose exec db psql -U postgres -d fortsight

# Run backend tests
test:
	docker-compose exec backend pytest

# Clean up volumes (WARNING: Deletes database data)
clean:
	docker-compose down -v
