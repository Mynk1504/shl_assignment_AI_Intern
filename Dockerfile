FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Render exposes the $PORT env variable. 
# We use the shell form of CMD so that the variable gets evaluated.
CMD uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
