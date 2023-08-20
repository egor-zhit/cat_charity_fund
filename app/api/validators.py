from http import HTTPStatus
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.charity_project import project_crud
from app.models.charity_project import CharityProject


async def check_name_duplicate(
        project_name: str,
        session: AsyncSession,
) -> None:
    project_id = await project_crud.get_project_id_by_name(project_name, session)
    if project_id is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Проект с таким именем уже существует!',
        )


async def check_project_exists(
        project_id: int,
        session: AsyncSession,
) -> CharityProject:
    project = await project_crud.get(
        project_id, session
    )
    if project is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Проект не найдена!'
        )
    return project


async def check_invested_amount(
        project_id: int,
        full_amount: int,
        session: AsyncSession,
) -> None:
    invested_amount = await project_crud.get_amount(project_id, session)
    if invested_amount is not None and full_amount < invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Сумма не может быть меньше уже внесенной!'
        )


async def check_the_project_before_updating(
        project_id: int,
        obj_in: CharityProject,
        session: AsyncSession,
):
    proj = await check_project_exists(project_id, session)
    if proj.fully_invested is True:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Закрытый проект нельзя редактировать!',
        )
    if obj_in.name is not None:
        await check_name_duplicate(obj_in.name, session)
    if obj_in.full_amount is not None:
        await check_invested_amount(project_id, obj_in.full_amount, session)
    return obj_in


async def check_the_project_before_deleting(
        project_id: int,
        session: AsyncSession
):
    project = await project_crud.get_amount(project_id, session)
    if project != 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='В проект были внесены средства, не подлежит удалению!',
        )
