from datetime import datetime, timezone
import requests
from utils.config import BTC_API_URL, EXCHANGE_API_URL

def fetch_and_store_btc_price(collection):
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
