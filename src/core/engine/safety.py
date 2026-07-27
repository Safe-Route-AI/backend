def compute_safety_score(features: dict) -> float:
    score = 100.0
    
    # Deterministic IF-THEN rules
    if features["hour"] >= 22 or features["hour"] <= 4:
        if features["lighting"] < 0.3 and features["incident_density"] > 0.5:
            score -= 60
        elif features["lighting"] < 0.5:
            score -= 30
            
    if features["incident_density"] > 0.7:
        score -= 40
    elif features["incident_density"] > 0.3:
        score -= 20
        
    if features["crowd_density"] < 0.2 and features["hour"] >= 20:
        score -= 15
        
    return max(0.0, min(100.0, score))

def aggregate_route_safety(segment_scores: list) -> float:
    if not segment_scores:
        return 0.0
    return sum(segment_scores) / len(segment_scores)