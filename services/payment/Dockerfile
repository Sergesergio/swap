FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY services/payment/ services/payment/
COPY shared/ shared/

ENV PYTHONPATH=/app
CMD ["uvicorn", "services.payment.main:app", "--host", "0.0.0.0", "--port", "8004"]