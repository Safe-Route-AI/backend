from flask import Blueprint, request, jsonify
from src.core.manager import process_route_request

routes_bp = Blueprint('routes', __name__)

@routes_bp.route('/routes', methods=['POST'])
def get_safe_route():
    data = request.get_json()
    origin = data.get('origin')
    destination = data.get('destination')
    
    if not origin or not destination:
        return jsonify({"error": "Origin and destination required"}), 400
        
    # Manager will handle routing, modules parallelization, and optimization
    best_route = process_route_request(origin, destination)
    
    return jsonify(best_route)