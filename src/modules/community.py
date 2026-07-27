from datetime import datetime, timedelta
from src.database.mongo import get_db

def get_community_features(lat: float, lon: float) -> dict:
    db = get_db()
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    
    # Query incidents within 200m radius
    query = {
        "location": {
            "$near": {
                "$geometry": {"type": "Point", "coordinates": [lon, lat]},
                "$maxDistance": 200
            }
        },
        "timestamp": {"$gte": thirty_days_ago}
    }
    
    incidents = list(db.incidents.find(query))
    report_count = len(incidents)
    
    if report_count == 0:
        return {"incident_density": 0.0, "severity_score": 0.0}
    
    avg_severity = sum(inc.get("severity", 1) for inc in incidents) / report_count
    
    # Normalize values
    incident_density = min(report_count / 10.0, 1.0) # Assuming 10 is max density
    severity_score = avg_severity / 5.0 # Assuming severity is out of 5
    
    return {
        "incident_density": incident_density,
        "severity_score": severity_score
    }