from datetime import datetime, timedelta, timezone

def delete_old_data(collection):
    twelve_months_ago = datetime.now(timezone.utc) - timedelta(days=365)
    result = collection.delete_many({"timestamp": {"$lt": twelve_months_ago}})
    print(f"Deleted {result.deleted_count} old records")
