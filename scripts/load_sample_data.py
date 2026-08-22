import os
import sys
from sqlalchemy.orm import Session
from backend.app.core.database import SessionLocal, engine
from backend.app.models.users import User
from backend.app.models.forts import Fort

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def load_sample_data(db: Session):
    # Check if data exists
    if db.query(User).first():
        print("Data already exists. Skipping load.")
        return

    print("Loading sample data...")
    # Add User
    test_user = User(name="Test User", email="test@example.com")
    db.add(test_user)
    
    # Add Fort (Raigad)
    raigad_wkt = "SRID=4326;POINT(73.5323 18.2346)"
    fort = Fort(
        name="Raigad Fort",
        marathi_name="रायगड",
        description="Capital of the Maratha Empire.",
        elevation=820.0,
        district="Raigad",
        difficulty="Moderate",
        best_season="Winter",
        geometry=raigad_wkt,
        source="Sample Data"
    )
    db.add(fort)
    
    db.commit()
    print("Sample data loaded successfully.")

if __name__ == "__main__":
    db = SessionLocal()
    try:
        load_sample_data(db)
    finally:
        db.close()
