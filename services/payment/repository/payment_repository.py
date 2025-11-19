from sqlmodel import Session, select
from typing import Optional
from datetime import datetime
from services.payment.models import Payment

class PaymentRepository:
    def __init__(self, session: Session):
        self.session = session

    async def hold_payment(self, offer_id: int, amount: float) -> Payment:
        payment = Payment(offer_id=offer_id, amount=amount, status="held")
        self.session.add(payment)
        self.session.commit()
        self.session.refresh(payment)
        return payment

    async def get_payment(self, payment_id: int) -> Optional[Payment]:
        statement = select(Payment).where(Payment.id == payment_id)
        result = self.session.execute(statement)
        return result.scalar_one_or_none()

    async def release_payment(self, payment_id: int) -> Optional[Payment]:
        payment = await self.get_payment(payment_id)
        if not payment:
            return None
        payment.status = "released"
        payment.updated_at = datetime.utcnow()
        self.session.commit()
        self.session.refresh(payment)
        return payment
