import pytest
from pydantic import ValidationError
from app.schemas.fort import FortCreate, FortResponse
from app.schemas.visibility import VisibilityRequest, VisibilityResponse

def test_fort_create_schema_valid():
    fort = FortCreate(
        name="Torna",
        latitude=18.27,
        longitude=73.62,
        elevation=1403.0
    )
    assert fort.name == "Torna"
    assert fort.latitude == 18.27

def test_fort_create_schema_invalid():
    with pytest.raises(ValidationError):
        FortCreate(
            name="Torna",
            latitude=200.0, # Invalid lat
            longitude=73.62,
            elevation=1403.0
        )

def test_visibility_request_schema():
    req = VisibilityRequest(
        observer_lat=18.0,
        observer_lon=73.0,
        target_lat=18.1,
        target_lon=73.1
    )
    assert req.observer_height == 1.7 # Default value
    
def test_visibility_request_schema_invalid():
    with pytest.raises(ValidationError):
        VisibilityRequest(
            observer_lat=-100.0, # Invalid
            observer_lon=73.0,
            target_lat=18.1,
            target_lon=73.1
        )
