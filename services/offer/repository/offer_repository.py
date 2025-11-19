from sqlmodel import Session, select
from typing import Optional, List
from datetime import datetime
import json
from services.offer.models import Offer, OfferMessage


class OfferRepository:
    def __init__(self, session: Session):
        self.session = session

    # create an offer
    async def create_offer(self, offer_create: "OfferCreate") -> Offer:
        # Convert Pydantic model to ORM model
        offer = Offer(
            listing_id=offer_create.listing_id,
            buyer_id=offer_create.buyer_id,
            seller_id=offer_create.seller_id,
            type=offer_create.type,
            price=offer_create.price,
            swap_listing_ids=json.dumps(offer_create.swap_listing_ids) if offer_create.swap_listing_ids else None,
            message=offer_create.message,
            expires_at=offer_create.expires_at
        )
        self.session.add(offer)
        self.session.commit()
        self.session.refresh(offer)
        return offer

    async def get_offer(self, offer_id: int) -> Optional[Offer]:
        statement = select(Offer).where(Offer.id == offer_id)
        result = self.session.execute(statement)
        return result.scalar_one_or_none()

    async def get_user_offers(self, user_id: int) -> List[Offer]:
        # returns offers where user is buyer or seller and not cancelled
        statement = select(Offer).where(
            (Offer.buyer_id == user_id) | (Offer.seller_id == user_id),
            Offer.status != "cancelled"
        )
        result = self.session.execute(statement)
        return result.scalars().all()

    async def update_offer_status(
        self,
        offer_id: int,
        status: str,
        message: Optional[str] = None
    ) -> Optional[Offer]:
        offer = await self.get_offer(offer_id)
        if not offer:
            return None

        offer.status = status
        offer.updated_at = datetime.utcnow()

        if message:
            offer_message = OfferMessage(
                offer_id=offer.id,
                sender_id=offer.seller_id,
                message=message
            )
            self.session.add(offer_message)

        self.session.commit()
        self.session.refresh(offer)
        return offer

    # message helpers
    async def create_offer_message(self, message: OfferMessage) -> OfferMessage:
        self.session.add(message)
        self.session.commit()
        self.session.refresh(message)
        return message

    async def get_offer_messages(self, offer_id: int) -> List[OfferMessage]:
        statement = select(OfferMessage).where(
            OfferMessage.offer_id == offer_id
        ).order_by(OfferMessage.created_at)
        result = self.session.execute(statement)
        return result.scalars().all()


class MessageRepository:
    def __init__(self, session: Session):
        self.session = session

    async def create(self, message: OfferMessage) -> OfferMessage:
        self.session.add(message)
        self.session.commit()
        self.session.refresh(message)
        return message

    async def get_by_offer(self, offer_id: int) -> List[OfferMessage]:
        statement = select(OfferMessage).where(
            OfferMessage.offer_id == offer_id
        ).order_by(OfferMessage.created_at)
        result = self.session.execute(statement)
        return result.scalars().all()