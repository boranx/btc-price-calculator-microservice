# commands/delete_old.py
from datetime import datetime, timedelta, timezone
from utils.db import get_db

def delete_old_data():
    client, db, collection = get_db()
    twelve_months_ago = datetime.now(timezone.utc) - timedelta(days=365)
    result = collection.delete_many({"timestamp": {"$lt": twelve_months_ago}})
    print(f"Deleted {result.deleted_count} old records")
