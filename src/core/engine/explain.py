def generate_explanation(features: dict) -> str:
    """
    Generates a human-readable explanation based on negative factors.
    """
    reasons = []
    
    if features.get("lighting", 1.0) < 0.3:
        reasons.append("Poor lighting (-35% contribution)")
    if features.get("crowd_density", 1.0) < 0.2:
        reasons.append("Low crowd density (-25% contribution)")
    if features.get("incident_density", 0.0) > 0.5:
        reasons.append("High historical incident density (-20% contribution)")
        
    if not reasons:
        return "Safe conditions observed."
        
    return "Safety reduced due to: " + ", ".join(reasons)