from fastapi import APIRouter
from typing import Any, List

router = APIRouter()

@router.get("/")
def get_forts() -> Any:
    """Retrieve forts."""
    # Placeholder
    return []

@router.get("/{fort_id}")
def get_fort(fort_id: int) -> Any:
    """Get fort by ID."""
    # Placeholder
    return {"id": fort_id, "name": "Dummy Fort"}
