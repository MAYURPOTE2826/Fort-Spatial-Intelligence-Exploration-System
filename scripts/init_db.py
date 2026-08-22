import asyncio
import os
import sys

# Add the parent directory to sys.path so we can import app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.app.core.database import Base, engine
from backend.app import models

def init_db():
    print("Creating tables (if not exist)...")
    # In a real production setup, we rely solely on Alembic.
    # This script is just for local testing / quick initialization.
    Base.metadata.create_all(bind=engine)
    print("Database initialized successfully.")

if __name__ == "__main__":
    init_db()
