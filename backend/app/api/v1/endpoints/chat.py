from fastapi import APIRouter, Depends, HTTPException, Request
from typing import Any, List, Optional
from pydantic import BaseModel
from sqlalchemy.orm import Session
import uuid

from app.core.database import get_db
from app.models.rag import ChatSession, ChatMessage
from app.services.query_classifier import query_classifier
from app.services.rag_retriever import rag_retriever
from app.services.llm_service import llm_service
from app.core.rate_limit import limiter

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    heading: Optional[float] = None

class Source(BaseModel):
    title: str
    url: Optional[str] = None

class VisibleFort(BaseModel):
    name: str
    distance: float
    id: Optional[int] = None

class ChatResponse(BaseModel):
    message: str
    sources: List[Source] = []
    visible_forts: List[VisibleFort] = []
    session_id: str

SYSTEM_PROMPT = """You are FortSight AI assistant, helping users explore Maharashtra forts.
Be helpful, accurate, and friendly.
Support Marathi language if the user speaks Marathi.
Always cite your sources using [Source: document title].
If asked about visible forts, use the provided context to list them clearly.

Context:
{context}

User location (optional): {lat}, {lon}
"""

@router.post("/", response_model=ChatResponse)
@limiter.limit("20/minute")
def chat_query(request: Request, payload: ChatRequest, db: Session = Depends(get_db)) -> Any:
    """Chat with RAG assistant."""
    
    # 1. Session Management
    session_id = payload.session_id
    if not session_id:
        session_id = str(uuid.uuid4())
        new_session = ChatSession(id=session_id)
        db.add(new_session)
        db.commit()
    else:
        session = db.query(ChatSession).filter(ChatSession.id == session_id).first()
        if not session:
            new_session = ChatSession(id=session_id)
            db.add(new_session)
            db.commit()

    # Save user message
    user_msg = ChatMessage(
        session_id=session_id,
        role="user",
        content=payload.message,
        latitude=payload.latitude,
        longitude=payload.longitude,
        heading=payload.heading
    )
    db.add(user_msg)
    db.commit()

    # 2. Query Classification
    query_type = query_classifier.classify(payload.message)
    
    # 3. Retrieve Context
    if query_type == "STATIC_KNOWLEDGE":
        retrieval_result = {"context": rag_retriever.retrieve_static(db, payload.message), "visible_forts": []}
    elif query_type == "SPATIAL_QUERY":
        retrieval_result = rag_retriever.retrieve_spatial(db, payload.message, payload.latitude, payload.longitude, payload.heading)
    else: # HYBRID_QUERY
        retrieval_result = rag_retriever.retrieve_hybrid(db, payload.message, payload.latitude, payload.longitude, payload.heading)
        
    context_data = retrieval_result.get("context", [])
    visible_forts_data = retrieval_result.get("visible_forts", [])
    
    # 4. Prepare prompt
    context_str = "\n\n".join([f"Title: {c.get('title')}\nContent: {c.get('content')}" for c in context_data])
    
    sys_prompt = SYSTEM_PROMPT.format(
        context=context_str,
        lat=payload.latitude or "Unknown",
        lon=payload.longitude or "Unknown"
    )
    
    # 5. Get LLM response
    llm_response = llm_service.generate_response(
        system_instruction=sys_prompt,
        user_prompt=payload.message
    )
    
    # Save assistant message
    asst_msg = ChatMessage(
        session_id=session_id,
        role="assistant",
        content=llm_response
    )
    db.add(asst_msg)
    db.commit()
    
    # 6. Format Response
    sources = []
    for c in context_data:
        if c.get("title") and c.get("title") != "Live Visibility Data":
            sources.append(Source(title=c["title"], url=c.get("source_url")))
            
    # Deduplicate sources
    unique_sources = {s.title: s for s in sources}.values()
    
    return ChatResponse(
        message=llm_response,
        sources=list(unique_sources),
        visible_forts=[VisibleFort(**vf) for vf in visible_forts_data],
        session_id=session_id
    )
