import os
from shared.kafka import KafkaConsumer
from repository.listing_repository import ListingRepository
from sqlmodel import Session
from repository.database import get_session
import logging

logger = logging.getLogger(__name__)

class ListingEventConsumer:
    def __init__(self):
        self.consumer = KafkaConsumer(
            bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVERS"),
            group_id="listing-service",
            topics=["user.verified", "offer.accepted"]
        )
    
    async def start(self):
        # Register handlers
        self.consumer.add_handler("user.verified", self.handle_user_verified)
        self.consumer.add_handler("offer.accepted", self.handle_offer_accepted)
        await self.consumer.start()
    
    async def stop(self):
        await self.consumer.stop()
    
    async def handle_user_verified(self, data: dict):
        """When a user is verified, update their listings to show verified status"""
        try:
            session = next(get_session())
            repository = ListingRepository(session)
            
            # Get all user's listings
            listings = await repository.get_by_user_id(data["user_id"])
            
            # Update each listing (could be optimized with bulk update)
            for listing in listings:
                listing.seller_verified = True
                await repository.update(listing.id, listing)
            
            logger.info(f"Updated verified status for listings of user {data['user_id']}")
        except Exception as e:
            logger.error(f"Error handling user.verified event: {e}")
    
    async def handle_offer_accepted(self, data: dict):
        """When an offer is accepted, mark the listing as sold"""
        try:
            session = next(get_session())
            repository = ListingRepository(session)
            
            # Update listing status
            listing = await repository.get_by_id(data["listing_id"])
            if listing:
                listing.status = "sold"
                await repository.update(listing.id, listing)
                logger.info(f"Marked listing {data['listing_id']} as sold")
            else:
                logger.warning(f"Listing {data['listing_id']} not found")
        except Exception as e:
            logger.error(f"Error handling offer.accepted event: {e}")