# Installation Guide

This guide covers setting up FortSight AI for local development.

## Prerequisites

- **Python 3.11+**
- **Node.js 20+**
- **PostgreSQL 14+** (with `pgvector` extension)
- **Redis**
- **Git**

## Backend Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/MAYURPOTE2826/Fort-Spatial-Intelligence-Exploration-System.git
   cd Fort-Spatial-Intelligence-Exploration-System/backend
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables:**
   Copy `.env.development.example` to `.env` and fill in your database credentials and API keys.

5. **Run Migrations (if applicable):**
   ```bash
   alembic upgrade head
   ```

6. **Start the Development Server:**
   ```bash
   uvicorn app.main:app --reload
   ```

## Frontend Setup

1. **Navigate to the frontend directory:**
   ```bash
   cd ../frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Environment Variables:**
   If the backend is not on `localhost:8000`, configure `VITE_API_URL` in a `.env` file.

4. **Start the Development Server:**
   ```bash
   npm run dev
   ```
