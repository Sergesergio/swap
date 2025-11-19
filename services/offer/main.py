from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import logging

from services.offer.routers import offer
from services.offer.events.consumer import OfferEventConsumer
from services.offer.events.producer import OfferEventProducer
from services.offer.repository.offer_repository import OfferRepository
from shared.database import init_db, get_session

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="Swap Offer Service")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(offer.router, prefix="/api/v1", tags=["offers"])

# Startup event handler
@app.on_event("startup")
async def startup_event():
    # Initialize database
    init_db()
    
    # Initialize and start Kafka producer
    producer = OfferEventProducer()
    await producer.start()
    
    # Initialize and start Kafka consumer
    session = next(get_session())
    offer_repository = OfferRepository(session)
    consumer = OfferEventConsumer(offer_repository)
    await consumer.start()
    
    logger.info("Offer service started successfully")

# Shutdown event handler
@app.on_event("shutdown")
async def shutdown_event():
    # Cleanup Kafka connections
    producer = OfferEventProducer()
    await producer.stop()
    
    consumer = OfferEventConsumer(next(get_session()))
    await consumer.stop()
    
    logger.info("Offer service shutdown complete")

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8003)