import datetime
from flask import Blueprint, request, jsonify
from src.database.mongo import get_db

incidents_bp = Blueprint('incidents', __name__)

@incidents_bp.route('/incidents', methods=['POST'])
def report_incident():
    db = get_db()
    data = request.get_json()
    
    incident = {
        "location": {
            "type": "Point",
            "coordinates": [data['lon'], data['lat']]
        },
        "type": data['type'],
        "severity": data.get('severity', 1),
        "timestamp": datetime.datetime.utcnow()
    }
    
    db.incidents.insert_one(incident)
    return jsonify({"message": "Incident reported"}), 201

@incidents_bp.route('/incidents', methods=['GET'])
def get_incidents():
    db = get_db()
    incidents = list(db.incidents.find({}, {'_id': 0}).limit(100))
    return jsonify(incidents)