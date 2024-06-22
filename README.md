

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