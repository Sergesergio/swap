FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY services/admin/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY services/admin /app
COPY shared /app/shared

# Create necessary directories
RUN mkdir -p /app/staticfiles /app/logs

# Collect static files
RUN python manage.py collectstatic --noinput || true

# Health check
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD curl -f http://localhost:8005/health/ || exit 1

# Expose port
EXPOSE 8005

# Run Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8005", "--workers", "4", "--timeout", "120", "config.wsgi:application"]
