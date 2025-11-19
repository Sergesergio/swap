from sqlmodel import Session, select
from typing import Optional
from models import Wallet

class WalletRepository:
    def __init__(self, session: Session):
        self.session = session
    
    async def create(self, wallet: Wallet) -> Wallet:
        self.session.add(wallet)
        await self.session.commit()
        await self.session.refresh(wallet)
        return wallet
    
    async def get_by_id(self, wallet_id: int) -> Optional[Wallet]:
        statement = select(Wallet).where(Wallet.id == wallet_id)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()
    
    async def get_by_user_id(self, user_id: int) -> Optional[Wallet]:
        statement = select(Wallet).where(Wallet.user_id == user_id)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()
    
    async def update_balance(
        self,
        wallet_id: int,
        balance: float,
        locked_balance: float
    ) -> Wallet:
        wallet = await self.get_by_id(wallet_id)
        if not wallet:
            return None
        
        wallet.balance = balance
        wallet.locked_balance = locked_balance
        
        await self.session.commit()
        await self.session.refresh(wallet)
        return wallet