from app.core.db import AsyncSessionLocal
from sqlalchemy import select
from app.crud.base import CRUDBase
from app.models import Donations, User
from app.models.donation import Donations


class CRUDDonation(CRUDBase):
    async def get_by_user(
            self, session: AsyncSessionLocal, user: User
    ):
        reservations = await session.execute(
            select(Donations).where(
                Donations.user_id == user.id
            )
        )
        return reservations.scalars().all()


donation_crud = CRUDDonation(Donations)