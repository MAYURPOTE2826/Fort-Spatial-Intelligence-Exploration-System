from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from geoalchemy2 import Geometry
from app.core.database import Base

class TerrainTile(Base):
    __tablename__ = "terrain_tiles"

    id = Column(Integer, primary_key=True, index=True)
    tile_name = Column(String, index=True, nullable=False, unique=True)
    zoom_level = Column(Integer, nullable=False)
    # Bounding box or geometry covered by this tile
    geometry = Column(Geometry('POLYGON', srid=4326), nullable=False)
    file_path = Column(String, nullable=False)
    resolution_m = Column(Float)
    source = Column(String, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
