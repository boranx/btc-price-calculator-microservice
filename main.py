# main.py
from flask import Flask
import threading
import schedule
import time
from commands.fetch_store import fetch_and_store_btc_price
from commands.delete_old import delete_old_data
from queries.get_price import get_btc_price

app = Flask(__name__)

# Scheduler for fetching BTC prices
schedule.every(5).minutes.do(fetch_and_store_btc_price)
# Scheduler for deleting old data
schedule.every().day.at("00:00").do(delete_old_data)

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

threading.Thread(target=run_scheduler).start()

@app.route('/btc-price', methods=['GET'])
def btc_price_endpoint():
    return get_btc_price()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
