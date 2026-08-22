from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

# Historical Document
class HistoricalDocumentBase(BaseModel):
    title: str
    content: str
    source_url: Optional[str] = None
    fort_id: Optional[int] = None

class HistoricalDocumentCreate(HistoricalDocumentBase):
    pass

class HistoricalDocumentResponse(HistoricalDocumentBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Document Chunk
class DocumentChunkBase(BaseModel):
    chunk_index: int
    content: str
    embedding: Optional[List[float]] = None

class DocumentChunkCreate(DocumentChunkBase):
    document_id: int

class DocumentChunkResponse(DocumentChunkBase):
    id: int
    document_id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Chat Session
class ChatSessionBase(BaseModel):
    pass

class ChatSessionCreate(ChatSessionBase):
    user_id: int

class ChatSessionResponse(ChatSessionBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Chat Message
class ChatMessageBase(BaseModel):
    role: str
    content: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    heading: Optional[float] = None

class ChatMessageCreate(ChatMessageBase):
    session_id: int

class ChatMessageResponse(ChatMessageBase):
    id: int
    session_id: int
    created_at: datetime

    class Config:
        from_attributes = True
