from fastapi import APIRouter, UploadFile, File, Form, Depends
from typing import Any, Dict

from app.services.ml.fort_classifier import fort_classifier
from app.services.ml.visibility_confidence import visibility_confidence
from app.services.ml.trek_difficulty import trek_difficulty
from app.services.ml.landmark_recognizer import landmark_recognizer

router = APIRouter()

@router.post("/recognize-fort")
async def recognize_fort(file: UploadFile = File(...)) -> Dict[str, Any]:
    """Identify fort from an uploaded image."""
    image_bytes = await file.read()
    return fort_classifier.predict(image_bytes)

@router.post("/visibility-confidence")
def get_visibility_confidence(distance_km: float, dem_resolution_m: float, terrain_ruggedness: float) -> Dict[str, Any]:
    """Predict confidence of visibility."""
    return visibility_confidence.predict_confidence(distance_km, dem_resolution_m, terrain_ruggedness)

@router.post("/trek-difficulty")
def get_trek_difficulty(elevation_gain_m: float, distance_km: float, terrain_type: str) -> Dict[str, Any]:
    """Predict trek difficulty based on trail data."""
    return trek_difficulty.predict_difficulty(elevation_gain_m, distance_km, terrain_type)

@router.post("/recognize-landmark")
async def recognize_landmark(file: UploadFile = File(...)) -> Dict[str, Any]:
    """Identify landmark structure type from an uploaded image."""
    image_bytes = await file.read()
    return landmark_recognizer.predict(image_bytes)
