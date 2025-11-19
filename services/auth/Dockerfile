FROM python:3.12-slim

WORKDIR /app

# Ensure /app is on the Python import path so imports like `shared.*` resolve
ENV PYTHONPATH=/app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY services/auth /app
COPY shared /app/shared

# Run service with explicit PYTHONPATH to ensure subprocess inherits it
ENV PYTHONPATH=/app
CMD ["sh", "-c", "PYTHONPATH=/app uvicorn main:app --host 0.0.0.0 --port 8000"]