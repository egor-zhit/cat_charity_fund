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
            status_code=400,
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
            status_code=404,
            detail='Проект не найдена!'
        )
    return project


async def chec_invested_amount(
        project_id: int,
        full_amount: int,
        session: AsyncSession,
) -> None:
    invested_amount = await project_crud.get_amount(project_id, session)
    if invested_amount is not None and full_amount < invested_amount:
        raise HTTPException(
            status_code=400,
            detail='Сумма не может быть меньше уже внесенной!'
        )


async def for_path_project(
        project_id: int,
        obj_in: CharityProject,
        session: AsyncSession,
):
    if obj_in.name is not None:
        await check_name_duplicate(obj_in.name, session)
    if obj_in.full_amount is not None:
        await chec_invested_amount(project_id, obj_in.full_amount, session)
    return obj_in


async def for_remove_project(
        project_id: int,
        session: AsyncSession
):
    project = await project_crud.get_amount(project_id, session)
    if project != 0:
        raise HTTPException(
            status_code=422,
            detail='Нельзя удалить проект в который уже внесены пожертвования!',
        )
