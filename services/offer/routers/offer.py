from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlmodel import Session

from services.offer.models import (
    OfferCreate,
    OfferRead,
    OfferUpdate,
    OfferMessageCreate,
    OfferMessageRead
)
from services.offer.repository.offer_repository import OfferRepository
from shared.database import get_session
from shared.auth import get_current_user, User

router = APIRouter()

@router.post("/offers/", response_model=OfferRead)
async def create_offer(
    offer: OfferCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Create a new offer"""
    offer_repo = OfferRepository(session)
    
    # Verify user is either buyer or seller
    if current_user.id not in [offer.buyer_id, offer.seller_id]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only create offers for yourself"
        )
    
    created_offer = await offer_repo.create_offer(offer)
    
    # TODO: Emit offer created event
    # await producer.offer_created(...)
    
    return created_offer

@router.get("/offers/{offer_id}", response_model=OfferRead)
async def get_offer(
    offer_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Get an offer by ID"""
    offer_repo = OfferRepository(session)
    offer = await offer_repo.get_offer(offer_id)
    
    if not offer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Offer not found"
        )
    
    # Verify user is involved in the offer
    if current_user.id not in [offer.buyer_id, offer.seller_id]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only view your own offers"
        )
    
    return offer

@router.get("/offers/user/{user_id}", response_model=List[OfferRead])
async def get_user_offers(
    user_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Get all offers for a user (as buyer or seller)"""
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only view your own offers"
        )
    
    offer_repo = OfferRepository(session)
    offers = await offer_repo.get_user_offers(user_id)
    return offers

@router.post("/offers/{offer_id}/accept", response_model=OfferRead)
async def accept_offer(
    offer_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Accept an offer"""
    offer_repo = OfferRepository(session)
    offer = await offer_repo.get_offer(offer_id)
    
    if not offer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Offer not found"
        )
    
    # Only seller can accept offer
    if current_user.id != offer.seller_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the seller can accept offers"
        )
    
    # Update offer status
    updated_offer = await offer_repo.update_offer_status(offer_id, "accepted")
    
    # TODO: Emit offer accepted event & request payment hold
    # await producer.offer_accepted(...)
    # await producer.payment_hold_request(...)
    
    return updated_offer

@router.post("/offers/{offer_id}/reject", response_model=OfferRead)
async def reject_offer(
    offer_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Reject an offer"""
    offer_repo = OfferRepository(session)
    offer = await offer_repo.get_offer(offer_id)
    
    if not offer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Offer not found"
        )
    
    # Only seller can reject offer
    if current_user.id != offer.seller_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the seller can reject offers"
        )
    
    # Update offer status
    updated_offer = await offer_repo.update_offer_status(offer_id, "rejected")
    
    # TODO: Emit offer rejected event
    # await producer.offer_rejected(...)
    
    return updated_offer

@router.post("/offers/{offer_id}/messages/", response_model=OfferMessageRead)
async def create_offer_message(
    offer_id: int,
    message: OfferMessageCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Add a message to an offer"""
    offer_repo = OfferRepository(session)
    offer = await offer_repo.get_offer(offer_id)
    
    if not offer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Offer not found"
        )
    
    # Verify user is involved in the offer
    if current_user.id not in [offer.buyer_id, offer.seller_id]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only message on your own offers"
        )
    
    message.offer_id = offer_id
    message.user_id = current_user.id
    
    created_message = await offer_repo.create_offer_message(message)
    return created_message

@router.get("/offers/{offer_id}/messages/", response_model=List[OfferMessageRead])
async def get_offer_messages(
    offer_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Get all messages for an offer"""
    offer_repo = OfferRepository(session)
    offer = await offer_repo.get_offer(offer_id)
    
    if not offer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Offer not found"
        )
    
    # Verify user is involved in the offer
    if current_user.id not in [offer.buyer_id, offer.seller_id]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only view messages on your own offers"
        )
    
    messages = await offer_repo.get_offer_messages(offer_id)
    return messages