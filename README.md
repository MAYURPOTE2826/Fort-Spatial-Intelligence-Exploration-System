# FortSight AI

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Docker](https://img.shields.io/badge/docker-ready-blue.svg)
![Python](https://img.shields.io/badge/python-3.11-blue.svg)
![React](https://img.shields.io/badge/react-18-blue.svg)

**FortSight AI** is an advanced Spatial Intelligence Exploration System designed to provide highly accurate, 3D-aware geospatial analytics and AI-powered insights for ancient hill forts.

## Core Features

- **Spatial Visibility Engine**: Calculates Line of Sight (LOS) between forts leveraging robust digital elevation models (DEM).
- **RAG-powered Chatbot**: An AI assistant embedded with Marathi language capabilities and RAG processing for answering queries about fort histories and architecture.
- **Dynamic 3D-Aware Mapping**: Visualizing forts, topography, and real-time visibility scores on interactive React-Leaflet maps.
- **Production Grade Architecture**: Containerized deployment employing Nginx, FastAPI, Gunicorn, PostgreSQL (with pgvector), and Redis.

## Documentation Navigation

Our comprehensive documentation is split into several guides to help you get started quickly and securely:

- [Installation Guide](docs/INSTALLATION.md): For setting up the development environment locally.
- [Deployment Guide](docs/DEPLOYMENT.md): For taking FortSight AI into production.
- [Architecture Overview](docs/ARCHITECTURE.md): Deep dive into the system's components and ML strategies.
- [API Reference](docs/API_REFERENCE.md): Documentation on exposed REST endpoints.
- [Contributing](docs/CONTRIBUTING.md): Guidelines on how to contribute to this project.
- [Troubleshooting](docs/TROUBLESHOOTING.md): Common errors and their resolutions.
- [FAQ](docs/FAQ.md): Frequently asked questions.

## Quick Start (Production)

The fastest way to deploy FortSight AI in a production environment is using our pre-configured Docker Compose setup:

```bash
# Clone the repository
git clone https://github.com/MAYURPOTE2826/Fort-Spatial-Intelligence-Exploration-System.git
cd Fort-Spatial-Intelligence-Exploration-System

# Set up environment variables
cp .env.production.example .env
nano .env # Configure your secrets and API keys

# Launch the system
docker-compose build
docker-compose up -d
```

Access the frontend application via `http://localhost` (or your domain name) and the backend API at `http://localhost/api/` (or `http://localhost:8000`).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
