# utils/db.py
import os
from pymongo import MongoClient

def get_db():
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
    DB_NAME = "crypto_data"
    COLLECTION_NAME = "btc_prices"
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]
    return client, db, collection
