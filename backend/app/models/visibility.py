from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, String, Index
from sqlalchemy.sql import func
from app.core.database import Base

class VisibilityResult(Base):
    __tablename__ = "visibility_results"

    id = Column(Integer, primary_key=True, index=True)
    observer_lat = Column(Float, nullable=False, index=True)
    observer_lon = Column(Float, nullable=False, index=True)
    observer_elevation = Column(Float, nullable=False)
    
    fort_id = Column(Integer, ForeignKey("forts.id", ondelete="CASCADE"), nullable=False, index=True)
    
    visibility_status = Column(String, nullable=False)
    visibility_score = Column(Float, nullable=False)
    
    calculated_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=False, index=True)

    # Composite index for quick spatial + fort lookup might be useful, 
    # but individual indexes should suffice for most query planners.
