from fastapi import APIRouter
from typing import Any, List

router = APIRouter()

# Dummy forts near Pune
MOCK_FORTS = [
    {
        "id": 1,
        "name": "Sinhagad Fort",
        "latitude": 18.3663,
        "longitude": 73.7559,
        "description": "A historic fortress located roughly 30 km southwest of the city of Pune."
    },
    {
        "id": 2,
        "name": "Shaniwar Wada",
        "latitude": 18.5195,
        "longitude": 73.8553,
        "description": "Historical fortification in the city of Pune."
    },
    {
        "id": 3,
        "name": "Lohagad Fort",
        "latitude": 18.7060,
        "longitude": 73.4770,
        "description": "One of the many hill forts of Maharashtra state in India, situated close to the hill station Lonavala."
    }
]

@router.get("/")
def get_forts() -> Any:
    """Retrieve forts."""
    return {"items": MOCK_FORTS, "total": len(MOCK_FORTS)}

@router.get("/{fort_id}")
def get_fort(fort_id: int) -> Any:
    """Get fort by ID."""
    fort = next((f for f in MOCK_FORTS if f["id"] == fort_id), None)
    if fort:
        return fort
    return {"id": fort_id, "name": "Dummy Fort"}
