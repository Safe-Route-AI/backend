def optimize_routes(routes_data: list, alpha: float = 0.5) -> dict:
    """
    Selects the best route based on safety and travel time.
    routes_data should be a list of dicts: {"route": path, "safety": 90, "time": 10}
    """
    if not routes_data:
        return None
        
    t_max = max(r["time"] for r in routes_data) if routes_data else 1
    
    best_route = None
    best_score = -1
    
    for route in routes_data:
        s_r = route["safety"] / 100.0
        t_r = route["time"]
        
        # score_opt(r) = alpha * S_r + (1 - alpha) * (1 - (T_r / T_max))
        score_opt = (alpha * s_r) + ((1 - alpha) * (1 - (t_r / t_max)))
        
        route["optimization_score"] = score_opt
        if score_opt > best_score:
            best_score = score_opt
            best_route = route
            
    return best_route