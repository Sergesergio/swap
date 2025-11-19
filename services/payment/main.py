from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from services.payment.routers import payment
from services.payment.events.producer import PaymentEventProducer
from services.payment.events.consumer import PaymentEventConsumer
from services.payment.repository.database import init_db, get_session
from services.payment.repository.payment_repository import PaymentRepository

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Swap Payment Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(payment.router, prefix="/api/v1", tags=["payments"])

@app.on_event("startup")
async def startup_event():
    # Init DB
    init_db()

    # Start producer
    producer = PaymentEventProducer()
    await producer.start()

    # Start consumer
    session = next(get_session())
    payment_repository = PaymentRepository(session)
    consumer = PaymentEventConsumer(payment_repository)
    await consumer.start()

@app.on_event("shutdown")
async def shutdown_event():
    producer = PaymentEventProducer()
    await producer.stop()
    
    session = next(get_session())
    consumer = PaymentEventConsumer(PaymentRepository(session))
    await consumer.stop()

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8004)
