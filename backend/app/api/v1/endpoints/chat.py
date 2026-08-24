from fastapi import APIRouter
from typing import Any

router = APIRouter()

@router.post("/query")
def chat_query(query: str) -> Any:
    """Chat with RAG assistant."""
    # Placeholder
    return {"response": f"Echo: {query}"}
