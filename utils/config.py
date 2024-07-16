import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DB_NAME = "crypto_data"
COLLECTION_NAME = "btc_prices"
API_KEY = os.getenv("API_KEY", "very_secret_api_key")
BTC_API_URL = "https://api.coindesk.com/v1/bpi/currentprice.json"
EXCHANGE_API_URL = "https://api.exchangerate-api.com/v4/latest/EUR"
