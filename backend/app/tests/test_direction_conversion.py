import pytest
from app.gis.direction_engine import get_cardinal_direction, calculate_relative_angle, is_in_field_of_view

def test_get_cardinal_direction():
    assert get_cardinal_direction(0) == "N"
    assert get_cardinal_direction(360) == "N"
    assert get_cardinal_direction(90) == "E"
    assert get_cardinal_direction(180) == "S"
    assert get_cardinal_direction(270) == "W"
    assert get_cardinal_direction(45) == "NE"
    assert get_cardinal_direction(22) == "NNE"
    assert get_cardinal_direction(-90) == "W"

def test_calculate_relative_angle():
    assert calculate_relative_angle(90, 0) == 90
    assert calculate_relative_angle(270, 0) == -90
    assert calculate_relative_angle(10, 350) == 20
    assert calculate_relative_angle(350, 10) == -20

def test_is_in_field_of_view():
    assert is_in_field_of_view(45, 0, fov=90) is True
    assert is_in_field_of_view(50, 0, fov=90) is False
    assert is_in_field_of_view(350, 0, fov=45) is True
