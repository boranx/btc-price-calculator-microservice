from flask import Flask
import threading
import schedule
import time
from pymongo import MongoClient
from utils.config import MONGO_URI, DB_NAME, COLLECTION_NAME
from commands.fetch_store import fetch_and_store_btc_price
from commands.delete_old import delete_old_data
from queries.get_price import get_btc_price

app = Flask(__name__)

# MongoDB Client Initialization
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

# Scheduler for fetching BTC prices
schedule.every(5).minutes.do(fetch_and_store_btc_price, collection=collection)
# Scheduler for deleting old data
schedule.every().day.at("00:00").do(delete_old_data, collection=collection)

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

threading.Thread(target=run_scheduler).start()

@app.route('/btc-price', methods=['GET'])
def btc_price_endpoint():
    return get_btc_price(collection)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
