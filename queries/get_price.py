from flask import request, jsonify
from datetime import datetime, timedelta, timezone
from utils.config import API_KEY
from queries.calculate_averages import calculate_averages

def get_prices_in_range(collection, start_date, end_date):
    return list(collection.find({"timestamp": {"$gte": start_date, "$lt": end_date}}))

def get_btc_price(collection):
    auth_header = request.headers.get('Authorization')
    if auth_header != f"Bearer {API_KEY}": 
        return jsonify({"error": "Unauthorized"}), 401

    now = datetime.now(timezone.utc)
    daily_start = now - timedelta(days=1)
    monthly_start = now - timedelta(days=30)

    daily_prices = get_prices_in_range(collection, daily_start, now)
    monthly_prices = get_prices_in_range(collection, monthly_start, now)

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
