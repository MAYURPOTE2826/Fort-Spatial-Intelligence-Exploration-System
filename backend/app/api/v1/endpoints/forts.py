from fastapi import APIRouter, HTTPException
from typing import Any

router = APIRouter()

MOCK_FORTS_DETAILS = {
    1: {
        "id": 1,
        "name": "Sinhagad Fort",
        "marathi_name": "सिंहगड",
        "latitude": 18.3663,
        "longitude": 73.7559,
        "elevation": 1312,
        "district": "Pune",
        "difficulty": "Moderate",
        "best_season": "Monsoon / Winter",
        "description": "Sinhagad is a hill fortress located at around 30 km southwest of the city of Pune, India. Some of the information available at this fort suggests that the fort could have been built 2000 years ago. The caves and the carvings in the Kaundinyeshwar temple stand as proofs for the same.",
        "history": "Previously known as Kondhana, the fort had been the site of many important battles, most notably the Battle of Sinhagad in 1670. Tanaji Malusare, a general of Chhatrapati Shivaji Maharaj, scaled the steep cliff using a monitor lizard (ghorpad) and recaptured the fort.",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/4/4e/Sinhagad_fort_Pune.jpg",
        "source": "Wikipedia",
        "architectural_style": "Yadava / Maratha Architecture",
        "built_by": "Kaundinya Rishi (Legend) / Yadavas",
        "interesting_facts": [
            "The fort was captured by Tanaji Malusare in 1670.",
            "Contains the memorial (Samadhi) of Tanaji Malusare.",
            "Has the tomb of Rajaram I, the younger son of Shivaji Maharaj.",
            "Famous for its 'Pitla Bhakri' and 'Kanda Bhaji' served by locals."
        ]
    }
}

MOCK_STRUCTURES = {
    1: [
        {
            "id": 101,
            "name": "Pune Darwaza",
            "type": "gate",
            "description": "The main entrance to the fort from the Pune side.",
            "historical_significance": "Historically the most heavily guarded entrance.",
            "latitude": 18.368,
            "longitude": 73.757
        },
        {
            "id": 102,
            "name": "Kalyan Darwaza",
            "type": "gate",
            "description": "Entrance from the Kalyan village side, often used for trekking.",
            "historical_significance": "Tanaji Malusare's forces are believed to have entered from a steep cliff near here.",
            "latitude": 18.364,
            "longitude": 73.754
        },
        {
            "id": 103,
            "name": "Dev Taki",
            "type": "water tank",
            "description": "A fresh water tank providing cold, sweet water year-round.",
            "historical_significance": "Served as the primary drinking water source for the garrison.",
            "latitude": 18.366,
            "longitude": 73.755
        },
        {
            "id": 104,
            "name": "Tanaji Samadhi",
            "type": "memorial",
            "description": "A memorial dedicated to the brave Maratha commander Tanaji Malusare.",
            "historical_significance": "Marks the place where he died fighting.",
            "latitude": 18.365,
            "longitude": 73.756
        }
    ]
}

MOCK_VIEWPOINTS = {
    1: [
        {
            "id": 201,
            "name": "Zunjar Machi",
            "direction": "South",
            "visible_features": ["Khadakwasla Dam", "Torna Fort (on clear days)"],
            "difficulty": "Easy",
            "time_to_visit": "15 mins from center",
            "latitude": 18.363,
            "longitude": 73.755
        },
        {
            "id": 202,
            "name": "Wind Point (Hawa Point)",
            "direction": "West",
            "visible_features": ["Sahyadri Ranges", "Sunset"],
            "difficulty": "Easy",
            "time_to_visit": "10 mins from center",
            "latitude": 18.365,
            "longitude": 73.753
        }
    ]
}

MOCK_TRAILS = {
    1: [
        {
            "id": 301,
            "name": "Atekar Vasti to Kalyan Darwaza",
            "start_point": "Atekar Vasti",
            "end_point": "Kalyan Darwaza",
            "distance_km": 2.5,
            "estimated_time_hours": 1.5,
            "difficulty": "Moderate",
            "elevation_gain": 600,
            "waypoints": [
                [18.355, 73.752],
                [18.360, 73.753],
                [18.364, 73.754]
            ]
        }
    ]
}

MOCK_CONNECTIONS = {
    1: [
        {
            "target_fort_id": 2,
            "target_fort_name": "Torna Fort",
            "distance_km": 14.5,
            "bearing_deg": 215,
            "historical_connection": "Both forts were key in Shivaji Maharaj's early conquests."
        },
        {
            "target_fort_id": 3,
            "target_fort_name": "Rajgad Fort",
            "distance_km": 18.0,
            "bearing_deg": 190,
            "historical_connection": "Rajgad was the first capital, heavily reliant on Sinhagad for defense."
        }
    ]
}


@router.get("/")
def get_forts() -> Any:
    """Retrieve all forts overview."""
    forts_list = []
    for f_id, data in MOCK_FORTS_DETAILS.items():
        forts_list.append({
            "id": data["id"],
            "name": data["name"],
            "marathi_name": data["marathi_name"],
            "latitude": data["latitude"],
            "longitude": data["longitude"],
            "description": data["description"]
        })
    # Add dummy fallbacks for listing if they are not fully detailed
    if len(forts_list) < 3:
        forts_list.append({"id": 2, "name": "Torna Fort", "latitude": 18.2778, "longitude": 73.6217, "description": "The first fort captured by Shivaji Maharaj."})
        forts_list.append({"id": 3, "name": "Rajgad Fort", "latitude": 18.2472, "longitude": 73.6822, "description": "The capital of the Maratha Empire."})

    return {"items": forts_list, "total": len(forts_list)}

@router.get("/{fort_id}")
def get_fort(fort_id: int) -> Any:
    """Get fort details by ID."""
    if fort_id in MOCK_FORTS_DETAILS:
        return MOCK_FORTS_DETAILS[fort_id]
    
    # Fallback mock for others
    return {
        "id": fort_id,
        "name": f"Mock Fort {fort_id}",
        "latitude": 18.5,
        "longitude": 73.8,
        "description": "Details not available in mock data."
    }

@router.get("/{fort_id}/structures")
def get_fort_structures(fort_id: int) -> Any:
    """Get internal structures of a fort."""
    return {"items": MOCK_STRUCTURES.get(fort_id, [])}

@router.get("/{fort_id}/viewpoints")
def get_fort_viewpoints(fort_id: int) -> Any:
    """Get viewpoints of a fort."""
    return {"items": MOCK_VIEWPOINTS.get(fort_id, [])}

@router.get("/{fort_id}/trails")
def get_fort_trails(fort_id: int) -> Any:
    """Get trails leading to/around a fort."""
    return {"items": MOCK_TRAILS.get(fort_id, [])}

@router.get("/{fort_id}/connections")
def get_fort_connections(fort_id: int) -> Any:
    """Get connected/related forts."""
    return {"items": MOCK_CONNECTIONS.get(fort_id, [])}
