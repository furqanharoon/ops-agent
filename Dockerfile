FROM python:3.10.16-slim
WORKDIR /app
COPY requirements.txt .
RUN apt-get update && apt-get install -y libpq-dev && rm -rf /var/lib/apt/lists/* 
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD uvicorn api.main:app --host 0.0.0.0 --port 8000
