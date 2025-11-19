FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY services/listing /app
COPY shared /app/shared

# Run service
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8002", "--reload"]