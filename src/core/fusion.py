def assemble_feature_vector(context_feats: dict, community_feats: dict, env_feats: dict) -> dict:
    """
    Combines module outputs into a single dictionary for the rule engine.
    """
    return {
        "hour": context_feats.get("hour", 12),
        "area_type": context_feats.get("area_type", "Mixed"),
        "lighting": env_feats.get("lighting", 0.5),
        "crowd_density": env_feats.get("crowd_density", 0.5),
        "incident_density": community_feats.get("incident_density", 0.0),
        "severity_score": community_feats.get("severity_score", 0.0)
    }