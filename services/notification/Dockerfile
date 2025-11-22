FROM python:3.12-slim

WORKDIR /app

# Copy shared modules
COPY shared/ /app/shared/
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy service files
COPY services/notification/ /app/services/notification/

WORKDIR /app/services/notification

# Set environment variables
ENV PYTHONPATH=/app:$PYTHONPATH
ENV DATABASE_URL=postgresql://swap_user:swap_password@postgres:5432/notifications
ENV KAFKA_BOOTSTRAP_SERVERS=kafka:9092

EXPOSE 8007

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8007", "--reload"]
