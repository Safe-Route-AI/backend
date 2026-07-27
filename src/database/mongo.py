import os
from pymongo import MongoClient

def get_db():
    uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
    client = MongoClient(uri)
    return client.saferoute

def init_db():
    db = get_db()
    # Create spatial index for 200m radius queries
    db.incidents.create_index([("location", "2dsphere")])