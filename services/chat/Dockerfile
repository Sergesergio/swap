FROM python:3.12-slim

WORKDIR /app

# Copy shared modules
COPY shared/ /app/shared/
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy service files
COPY services/chat/ /app/services/chat/

WORKDIR /app/services/chat

# Set environment variables
ENV PYTHONPATH=/app:$PYTHONPATH
ENV CHAT_DATABASE_URL=postgresql://swap_user:swap_password@postgres:5432/chat
ENV KAFKA_BOOTSTRAP_SERVERS=kafka:9092

EXPOSE 8006

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8006", "--reload"]
