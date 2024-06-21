FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY app.py app.py

ENV MONGO_URI=mongodb://mongodb:27017/
ENV API_KEY=your_secret_api_key

CMD ["python", "app.py"]
