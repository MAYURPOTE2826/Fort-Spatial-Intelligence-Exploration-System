def get_cardinal_direction(bearing: float) -> str:
    """
    Converts a bearing in degrees (0-360) to a 16-point cardinal direction string.
    """
    bearing = (bearing + 360) % 360
    directions = [
        "N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
        "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"
    ]
    # Each direction represents a 22.5 degree slice
    # 360 / 16 = 22.5
    # Shift by 11.25 to align North correctly around 0 (348.75 to 11.25)
    index = int(((bearing + 11.25) % 360) / 22.5)
    return directions[index]

def calculate_relative_angle(target_bearing: float, user_heading: float) -> float:
    """
    Calculates the relative angle between the user's heading and the target's bearing.
    Returns a value between -180 and 180 degrees.
    Positive means target is to the right, negative means left.
    """
    target_bearing = (target_bearing + 360) % 360
    user_heading = (user_heading + 360) % 360
    
    diff = target_bearing - user_heading
    
    # Normalize to -180 to 180
    if diff > 180:
        diff -= 360
    elif diff < -180:
        diff += 360
        
    return diff

def is_in_field_of_view(target_bearing: float, user_heading: float, fov: float = 60.0) -> bool:
    """
    Determines if a target is within the user's field of view.
    fov is the total field of view in degrees (e.g., 60 means +/- 30 degrees from heading).
    """
    relative_angle = calculate_relative_angle(target_bearing, user_heading)
    half_fov = fov / 2.0
    
    return abs(relative_angle) <= half_fov
