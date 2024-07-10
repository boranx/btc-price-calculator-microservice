# app.py
from flask import Flask, request, jsonify
from pymongo import MongoClient
from datetime import datetime, timedelta, timezone
import requests
import threading
import schedule
import time
import os

app = Flask(__name__)

# Configuration
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DB_NAME = "crypto_data"
COLLECTION_NAME = "btc_prices"
API_KEY = os.getenv("API_KEY", "very_secret_api_key")
BTC_API_URL = "https://api.coindesk.com/v1/bpi/currentprice.json"
EXCHANGE_API_URL = "https://api.exchangerate-api.com/v4/latest/EUR"

# MongoDB Client
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

def fetch_and_store_btc_price():
    response = requests.get(BTC_API_URL)
    if response.status_code == 200:
        data = response.json()
        btc_price_eur = data['bpi']['EUR']['rate_float']

        # Fetch EUR to CZK conversion rate
        exchange_response = requests.get(EXCHANGE_API_URL)
        if exchange_response.status_code == 200:
            exchange_data = exchange_response.json()
            eur_to_czk = exchange_data['rates'].get('CZK')
            if eur_to_czk:
                btc_price_czk = btc_price_eur * eur_to_czk
            else:
                btc_price_czk = None
        else:
            btc_price_czk = None
        
        timestamp = datetime.now(timezone.utc)

        collection.insert_one({
            "timestamp": timestamp,
            "price_eur": btc_price_eur,
            "price_czk": btc_price_czk
        })
        print(f"Stored BTC prices at {timestamp}")
    else:
        print("Failed to fetch BTC price")

# Scheduler for fetching BTC prices
schedule.every(5).minutes.do(fetch_and_store_btc_price)

def delete_old_data():
    twelve_months_ago = datetime.now(timezone.utc) - timedelta(days=365)
    result = collection.delete_many({"timestamp": {"$lt": twelve_months_ago}})
    print(f"Deleted {result.deleted_count} old records")

# Scheduler for deleting old data
schedule.every().day.at("00:00").do(delete_old_data)

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

threading.Thread(target=run_scheduler).start()

def calculate_averages(prices):
    if not prices:
        return {"avg_eur": None, "avg_czk": None}
    avg_eur = sum(p['price_eur'] for p in prices) / len(prices)
    czk_prices = [p['price_czk'] for p in prices if p['price_czk'] is not None]
    avg_czk = sum(czk_prices) / len(czk_prices) if czk_prices else None
    return {"avg_eur": avg_eur, "avg_czk": avg_czk}

def get_prices_in_range(start_date, end_date):
    return list(collection.find({"timestamp": {"$gte": start_date, "$lt": end_date}}))

@app.route('/btc-price', methods=['GET'])
def get_btc_price():
    auth_header = request.headers.get('Authorization')
    print(auth_header)
    # Normally we'd use a more secure way to handle API keys
    # Like "the token received" could be checked against a list of valid tokens from an authentication database.
    if auth_header != f"Bearer {API_KEY}": 
        return jsonify({"error": "Unauthorized"}), 401

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
