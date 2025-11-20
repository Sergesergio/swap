from fastapi import APIRouter, Depends, HTTPException, status
from services.payment.repository.payment_repository import PaymentRepository
from services.payment.repository.database import get_session
from services.payment.models import PaymentHoldRequest, PaymentResponse
from shared.auth import get_current_user, User
from sqlmodel import Session

router = APIRouter()

@router.post("/payments/hold", response_model=PaymentResponse)
async def hold_payment(
    req: PaymentHoldRequest,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Simulate holding payment in escrow for an offer."""
    repo = PaymentRepository(session)
    payment = await repo.hold_payment(req.offer_id, req.amount)

    # TODO: Emit event via producer if available
    # await producer.payment_held(payment.id, payment.offer_id, payment.amount)

    return PaymentResponse(
        id=payment.id,
        offer_id=payment.offer_id,
        amount=payment.amount,
        status=payment.status,
        created_at=payment.created_at,
        updated_at=payment.updated_at
    )

@router.post("/payments/{payment_id}/release", response_model=PaymentResponse)
async def release_payment(
    payment_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    repo = PaymentRepository(session)
    payment = await repo.release_payment(payment_id)
    if not payment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payment not found")

    # TODO: Emit event via producer if available
    # await producer.payment_released(payment.id, payment.offer_id, payment.amount)

    return PaymentResponse(
        id=payment.id,
        offer_id=payment.offer_id,
        amount=payment.amount,
        status=payment.status,
        created_at=payment.created_at,
        updated_at=payment.updated_at
    )
