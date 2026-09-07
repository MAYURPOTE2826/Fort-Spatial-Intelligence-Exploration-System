from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import ARRAY
from pgvector.sqlalchemy import Vector
from app.core.database import Base

class HistoricalDocument(Base):
    __tablename__ = "historical_documents"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    source_url = Column(String)
    language = Column(String, default="en")
    fort_id = Column(Integer, ForeignKey("forts.id", ondelete="SET NULL"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    chunks = relationship("DocumentChunk", back_populates="document", cascade="all, delete-orphan")

class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("historical_documents.id", ondelete="CASCADE"), nullable=False)
    chunk_index = Column(Integer, nullable=False)
    content = Column(Text, nullable=False)
    
    # Using pgvector Vector(384)
    embedding = Column(Vector(384))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    document = relationship("HistoricalDocument", back_populates="chunks")

class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id = Column(String, primary_key=True, index=True) # Use UUID string
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True) # Allow anonymous
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    messages = relationship("ChatMessage", back_populates="session", cascade="all, delete-orphan")

class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, ForeignKey("chat_sessions.id", ondelete="CASCADE"), nullable=False)
    role = Column(String, nullable=False) # e.g. "user", "assistant", "system"
    content = Column(Text, nullable=False)
    
    # Optional geospatial context for the message
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    heading = Column(Float, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    session = relationship("ChatSession", back_populates="messages")
