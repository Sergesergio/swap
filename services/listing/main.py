from fastapi import FastAPI, Depends, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session
from typing import List, Optional
from datetime import datetime
import os

from models import (
    Category,
    Listing,
    ListingResponse,
    ListingCreate
)
from repository.database import get_session, init_db
from repository.category_repository import CategoryRepository
from repository.listing_repository import ListingRepository
from utils.storage import MinioStorage
from shared.exceptions import ResourceNotFound, ValidationError
from events.consumer import ListingEventConsumer
from events.producer import ListingEventProducer

app = FastAPI(title="Listing Service")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
storage = MinioStorage()
listing_consumer = None
listing_producer = None

@app.on_event("startup")
async def startup_event():
    global listing_consumer, listing_producer
    
    # Initialize database tables
    init_db()
    
    # Initialize MinIO
    await storage.create_bucket()
    
    # Start event handlers (create them now in async context)
    listing_consumer = ListingEventConsumer()
    listing_producer = ListingEventProducer()
    await listing_consumer.start()
    await listing_producer.start()

@app.on_event("shutdown")
async def shutdown_event():
    await listing_consumer.stop()
    await listing_producer.stop()

# Category endpoints
@app.post("/categories", response_model=Category)
async def create_category(
    category: Category,
    session: Session = Depends(get_session)
):
    repository = CategoryRepository(session)
    return repository.create(category)

@app.get("/categories", response_model=List[Category])
async def get_categories(session: Session = Depends(get_session)):
    repository = CategoryRepository(session)
    return repository.get_all()

@app.get("/categories/{category_id}", response_model=Category)
async def get_category(
    category_id: int,
    session: Session = Depends(get_session)
):
    repository = CategoryRepository(session)
    category = repository.get_by_id(category_id)
    if not category:
        raise ResourceNotFound(f"Category {category_id} not found")
    return category

# Listing endpoints
@app.post("/listings", response_model=ListingResponse)
async def create_listing(
    listing: ListingCreate,
    files: List[UploadFile] = File(...),
    session: Session = Depends(get_session)
):
    # Upload images to MinIO
    image_urls = []
    for file in files:
        image_url = await storage.upload_file(
            file.filename,
            file.file,
            content_type=file.content_type
        )
        image_urls.append(image_url)
    
    # Create listing
    repository = ListingRepository(session)
    listing_db = Listing(**listing.dict(exclude={"tags"}))
    result = await repository.create(listing_db, image_urls, listing.tags)
    
    # Publish event
    await listing_producer.listing_created(
        listing_id=result.id,
        user_id=result.user_id,
        data={
            "title": result.title,
            "price": result.price
        }
    )
    
    return result

@app.get("/listings", response_model=List[ListingResponse])
async def search_listings(
    query: Optional[str] = None,
    category_id: Optional[int] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    condition: Optional[str] = None,
    session: Session = Depends(get_session)
):
    repository = ListingRepository(session)
    return repository.search(
        query,
        category_id,
        min_price,
        max_price,
        condition
    )

@app.get("/listings/{listing_id}", response_model=ListingResponse)
async def get_listing(
    listing_id: int,
    session: Session = Depends(get_session)
):
    repository = ListingRepository(session)
    listing = repository.get_by_id(listing_id)
    if not listing:
        raise ResourceNotFound(f"Listing {listing_id} not found")
    
    # Increment views
    repository.increment_views(listing_id)
    return listing

@app.put("/listings/{listing_id}", response_model=ListingResponse)
async def update_listing(
    listing_id: int,
    listing_update: ListingCreate,
    session: Session = Depends(get_session)
):
    repository = ListingRepository(session)
    listing = repository.update(listing_id, listing_update)
    if not listing:
        raise ResourceNotFound(f"Listing {listing_id} not found")
    return listing

@app.delete("/listings/{listing_id}")
async def delete_listing(
    listing_id: int,
    session: Session = Depends(get_session)
):
    repository = ListingRepository(session)
    success = repository.delete(listing_id)
    if not success:
        raise ResourceNotFound(f"Listing {listing_id} not found")
    return {"message": "Listing deleted successfully"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}