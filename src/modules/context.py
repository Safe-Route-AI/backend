import datetime
from src.utils.classifiers import get_area_type

def get_context_features(lat: float, lon: float) -> dict:
    now = datetime.datetime.now()
    hour = now.hour
    is_weekend = now.weekday() >= 4 # Friday & Saturday in Egypt
    
    area_type = get_area_type(lat, lon)
    
    return {
        "hour": hour,
        "is_weekend": is_weekend,
        "area_type": area_type
    }