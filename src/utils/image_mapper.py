import os

def get_segment_image(lat: float, lon: float) -> str:
    """
    Returns a mocked local path for the street imagery based on coordinates.
    """
    # Fallback default image path in case mapping fails
    default_path = "data/street_imagery/default.jpg"
    
    # In a real scenario, this maps lat/lon to a specific file
    mapped_path = f"data/street_imagery/{round(lat, 3)}_{round(lon, 3)}.jpg"
    
    if os.path.exists(mapped_path):
        return mapped_path
    return default_path