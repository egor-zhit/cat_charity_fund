from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_user, current_superuser
from app.crud.donation import donation_crud
from app.models.user import User
from app.schemas.donation import DonationCreate, DonationDB
from app.services.universal_function import main_process_invest


router = APIRouter()


@router.post(
    '/',
    response_model=DonationDB,
    response_model_exclude={'invested_amount', 'fully_invested', 'user_id'},
    response_model_exclude_none=True
)
async def create_new_donation(
    donation: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    new_donation = await donation_crud.create(donation, session, user)
    new_donation = await main_process_invest(
        session, donation=new_donation
    )
    return new_donation


@router.get(
    '/',
    response_model=List[DonationDB],
    response_model_exclude={'close_date'},
    dependencies=[Depends(current_superuser)],
)
async def get_read_all_donation(
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    return await donation_crud.get_multi(session)


@router.get(
    '/my',
    response_model=List[DonationDB],
    response_model_exclude={
        'user_id', 'invested_amount', 'fully_invested',
        'close_date '
    },
    response_model_exclude_none=True
)
async def get_my_donation(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    my_donation = await donation_crud.get_by_user(
        session=session, user=user
    )
    return my_donation
