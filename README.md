# Btc Price Calculator
BPC retrieves the current price of Bitcoin (BTC) in EUR from the Coindesk API and calculates the equivalent price in CZK using the Exchange Rates API. It stores this data in MongoDB and provides endpoints to retrieve the current price and locally calculated daily and monthly averages

## Features
Following the CQRS principles, BPC is split into 2 parts:
- Batch Processing: it runs as a standalone job in a different thread, using python `schedulers` which makes database writes isolated which will occur in certain time intervals.
- Serving: The API is listening `/btc-price` endpoint and returns results without using cache mechanism.

## Development

To launch locally:

```sh
brew install virtualenv
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
export MONGO_URI=mongodb://localhost:27017/
export API_KEY=very_secret_api_key
python main.py
```
or all stack with single command
```sh
podman-compose up -d
```

## Examples
```sh
python main.py
 * Serving Flask app 'main'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://192.168.15.49:5000
Press CTRL+C to quit
Stored BTC prices at 2024-06-23 08:10:29.684364+00:00 # Note that interval is set to 5 seconds for development purposes
Stored BTC prices at 2024-06-23 08:10:35.730535+00:00
```

Then, at some point hit `/btc-price` to see averages and current prices.

```sh
curl --location 'http://127.0.0.1:5000/btc-price' \
--header 'Authorization: Bearer very_secret_api_key' # it strictly check if token is `very_secret_api_key` but normally we'd verify to see if its valid from auth database.
```

```sh
{
    "current_price_czk": 1500518.162052,
    "current_price_eur": 60189.2564,
    "daily_avg_czk": 1500505.44515928,
    "daily_avg_eur": 60188.746296000005,
    "data_time": "2024-06-23T08:13:05.480000", # latest ingestion time
    "monthly_avg_czk": 1500505.44515928,
    "monthly_avg_eur": 60188.746296000005,
    "request_time": "2024-06-23T08:13:09.847279+00:00"
}
```

## Deployment
```sh
kubectl apply -f kubernetes-deploy.yaml
kubectl get pods -n btc-namespace
```

The docker build should be done as well to get the image propogated in k8s
```sh
docker build -t boranx/btc-app:latest .
docker push boranx/btc-app:latest
```