# queries/get_price.py
import os
from flask import request, jsonify
from datetime import datetime, timedelta, timezone
from utils.db import get_db
from queries.calculate_averages import calculate_averages

API_KEY = os.getenv("API_KEY", "very_secret_api_key")

def get_prices_in_range(start_date, end_date):
    client, db, collection = get_db()
    return list(collection.find({"timestamp": {"$gte": start_date, "$lt": end_date}}))

def get_btc_price():
    auth_header = request.headers.get('Authorization')
    if auth_header != f"Bearer {API_KEY}": 
        return jsonify({"error": "Unauthorized"}), 401

    client, db, collection = get_db()
    now = datetime.now(timezone.utc)
    daily_start = now - timedelta(days=1)
    monthly_start = now - timedelta(days=30)

    daily_prices = get_prices_in_range(daily_start, now)
    monthly_prices = get_prices_in_range(monthly_start, now)

    daily_avg = calculate_averages(daily_prices)
    monthly_avg = calculate_averages(monthly_prices)

    latest_price_cursor = collection.find().sort("timestamp", -1).limit(1)
    latest_price = list(latest_price_cursor)

    if len(latest_price) == 0:
        return jsonify({"error": "No data available"}), 500

    latest_price = latest_price[0]

    result = {
        "current_price_eur": latest_price["price_eur"],
        "current_price_czk": latest_price["price_czk"],
        "request_time": now.isoformat(),
        "data_time": latest_price["timestamp"].isoformat(),
        "daily_avg_eur": daily_avg["avg_eur"],
        "daily_avg_czk": daily_avg["avg_czk"],
        "monthly_avg_eur": monthly_avg["avg_eur"],
        "monthly_avg_czk": monthly_avg["avg_czk"]
    }
    return jsonify(result)
