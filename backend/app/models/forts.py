from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from geoalchemy2 import Geometry
from app.core.database import Base

class Fort(Base):
    __tablename__ = "forts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    marathi_name = Column(String)  # Support for Marathi UTF-8
    description = Column(Text)
    geometry = Column(Geometry('POINT', srid=4326), nullable=False) # indexed by default in GeoAlchemy2
    elevation = Column(Float)  # in meters
    district = Column(String, index=True)
    difficulty = Column(String)
    best_season = Column(String)
    history = Column(Text)
    image_url = Column(String)
    source = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    viewpoints = relationship("FortViewpoint", back_populates="fort", cascade="all, delete-orphan")
    structures = relationship("FortStructure", back_populates="fort", cascade="all, delete-orphan")
    trails = relationship("FortTrail", back_populates="fort", cascade="all, delete-orphan")

class FortViewpoint(Base):
    __tablename__ = "fort_viewpoints"

    id = Column(Integer, primary_key=True, index=True)
    fort_id = Column(Integer, ForeignKey("forts.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)
    type = Column(String)
    geometry = Column(Geometry('POINT', srid=4326), nullable=False)
    elevation = Column(Float)
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    fort = relationship("Fort", back_populates="viewpoints")

class FortStructure(Base):
    __tablename__ = "fort_structures"

    id = Column(Integer, primary_key=True, index=True)
    fort_id = Column(Integer, ForeignKey("forts.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)
    type = Column(String)
    # Using GEOMETRY generic to allow both Point and Polygon if needed, or specific
    # In PostGIS, we can specify geometry type Geometry(Geometry, 4326) for generic
    geometry = Column(Geometry('GEOMETRY', srid=4326), nullable=False)
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    fort = relationship("Fort", back_populates="structures")

class FortTrail(Base):
    __tablename__ = "fort_trails"

    id = Column(Integer, primary_key=True, index=True)
    fort_id = Column(Integer, ForeignKey("forts.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)
    difficulty = Column(String)
    geometry = Column(Geometry('LINESTRING', srid=4326), nullable=False)
    distance_km = Column(Float)
    estimated_time_hours = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    fort = relationship("Fort", back_populates="trails")

class FortConnection(Base):
    __tablename__ = "fort_connections"

    source_fort_id = Column(Integer, ForeignKey("forts.id", ondelete="CASCADE"), primary_key=True)
    target_fort_id = Column(Integer, ForeignKey("forts.id", ondelete="CASCADE"), primary_key=True)
    distance_km = Column(Float)
    bearing_deg = Column(Float)
    visibility_status = Column(String) # e.g. "visible", "blocked"
    visibility_score = Column(Float)
    last_calculated_at = Column(DateTime(timezone=True))

    # To query from either side easily, we might need explicitly defined relations if needed,
    # but since it's just a connection table we can keep it simple.

