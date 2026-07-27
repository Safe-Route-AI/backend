from src.modules.context import get_context_features
from src.modules.community import get_community_features
from src.modules.environment.brightness import get_lighting_score
from src.modules.environment.crowd import get_crowd_density
from src.core.fusion import assemble_feature_vector
from src.core.engine.safety import compute_safety_score, aggregate_route_safety
from src.core.engine.explain import generate_explanation
from src.core.engine.optimizer import optimize_routes
from src.utils.image_mapper import get_segment_image

def process_route_request(origin, destination):
    # Mocking k candidate routes retrieval for the prototype
    candidate_routes = [
        {"id": 1, "segments": [{"lat": 30.04, "lon": 31.23}], "time": 10},
        {"id": 2, "segments": [{"lat": 30.041, "lon": 31.231}], "time": 12}
    ]
    
    processed_routes = []
    
    for route in candidate_routes:
        segment_scores = []
        route_explanations = []
        
        for segment in route['segments']:
            lat, lon = segment['lat'], segment['lon']
            
            # 1. Context Module
            ctx_feats = get_context_features(lat, lon)
            
            # 2. Community Module
            comm_feats = get_community_features(lat, lon)
            
            # 3. Environment Module
            img_path = get_segment_image(lat, lon)
            env_feats = {
                "lighting": get_lighting_score(img_path),
                "crowd_density": get_crowd_density(img_path)
            }
            
            # 4. Feature Fusion
            vector = assemble_feature_vector(ctx_feats, comm_feats, env_feats)
            
            # 5. Safety Engine
            score = compute_safety_score(vector)
            segment_scores.append(score)
            
            # Collect explanation if score is low
            if score < 80:
                route_explanations.append(generate_explanation(vector))
                
        # Aggregate
        route_safety = aggregate_route_safety(segment_scores)
        
        processed_routes.append({
            "route_id": route["id"],
            "safety": route_safety,
            "time": route["time"],
            "explanation": " | ".join(set(route_explanations)) if route_explanations else "Route is generally safe."
        })
        
    # 6. Route Optimisation
    best_route = optimize_routes(processed_routes, alpha=0.7)
    return best_route