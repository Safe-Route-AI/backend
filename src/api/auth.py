import os
import datetime
import bcrypt
import jwt
from flask import Blueprint, request, jsonify
from src.database.mongo import get_db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    db = get_db()
    data = request.get_json()
    
    if db.users.find_one({"email": data['email']}):
        return jsonify({"error": "User already exists"}), 400
        
    hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
    
    db.users.insert_one({
        "email": data['email'],
        "password": hashed_password
    })
    return jsonify({"message": "User registered successfully"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    db = get_db()
    data = request.get_json()
    user = db.users.find_one({"email": data['email']})
    
    if user and bcrypt.checkpw(data['password'].encode('utf-8'), user['password']):
        token = jwt.encode({
            'user': data['email'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }, os.getenv('JWT_SECRET', 'secret'), algorithm='HS256')
        return jsonify({"token": token})
        
    return jsonify({"error": "Invalid credentials"}), 401