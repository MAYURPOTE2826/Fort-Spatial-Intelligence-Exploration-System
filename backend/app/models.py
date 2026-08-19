from sqlalchemy import Column, Integer, String, Float
from geoalchemy2 import Geometry
from app.core.database import Base

class Fort(Base):
    __tablename__ = "forts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    base_elevation = Column(Float)  # Elevation in meters
    location = Column(Geometry('POINT', srid=4326))  # Lat/Lon point
