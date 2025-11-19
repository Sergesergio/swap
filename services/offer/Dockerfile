FROM python:3.12-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy service code
COPY services/offer/ services/offer/
COPY shared/ shared/

# Set environment variables
ENV PYTHONPATH=/app
ENV MODULE_NAME=services.offer.main
ENV VARIABLE_NAME=app
ENV PORT=8003

# Run the application
CMD ["uvicorn", "services.offer.main:app", "--host", "0.0.0.0", "--port", "8003"]