from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (check_name_duplicate, check_project_exists,
                                check_the_project_before_updating,
                                check_the_project_before_deleting)
from app.core.user import current_superuser
from app.core.db import get_async_session
from app.crud.charity_project import project_crud
from app.schemas.charity_project import ProjectCreate, ProjectDB, ProjectUpdate
from app.services.universal_function import main_process_invest

router = APIRouter()


@router.post(
    '/',
    response_model=ProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_new_project(
    project: ProjectCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    await check_name_duplicate(project.name, session)
    new_project = await project_crud.create(project, session)
    new_project = await main_process_invest(
        session, project=new_project
    )
    return new_project


@router.get(
    '/',
    response_model=List[ProjectDB],
    response_model_exclude_none=True
)
async def get_all_project(
    session: AsyncSession = Depends(get_async_session),
):
    return await project_crud.get_multi(session)


@router.patch(
    '/{project_id}',
    response_model=ProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def partially_update_project(
    project_id: int,
    obj_in: ProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    project = await check_project_exists(project_id, session)
    obj = await check_the_project_before_updating(project_id, obj_in, session)
    project = await project_crud.update(
        project, obj, session
    )
    return project


@router.delete(
    '/{project_id}',
    response_model=ProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def delete_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    project_get = await check_project_exists(project_id, session)
    project = await check_the_project_before_deleting(project_id, session)
    project = await project_crud.remove(project_get, session)
    return project
