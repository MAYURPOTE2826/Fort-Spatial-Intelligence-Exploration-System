import pytest
from app.core.database import Base
from app.models.fort import Fort
from app.models.terrain import TerrainProfile
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def test_fort_model():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    fort = Fort(
        id=1,
        name="Rajgad",
        marathi_name="राजगड",
        description="A beautiful fort",
        type="Hill Fort",
        latitude=18.24,
        longitude=73.68,
        elevation=1376.0,
        difficulty="Tough"
    )
    session.add(fort)
    session.commit()
    
    fetched = session.query(Fort).filter_by(name="Rajgad").first()
    assert fetched is not None
    assert fetched.marathi_name == "राजगड"
    assert fetched.elevation == 1376.0

def test_terrain_profile_model():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    profile = TerrainProfile(
        id=1,
        source_lat=18.0,
        source_lon=73.0,
        target_lat=18.1,
        target_lon=73.1,
        highest_point_elevation=1000.0,
        average_elevation=800.0,
        ruggedness_index=0.5
    )
    session.add(profile)
    session.commit()
    
    fetched = session.query(TerrainProfile).first()
    assert fetched is not None
    assert fetched.highest_point_elevation == 1000.0
