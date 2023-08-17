from datetime import datetime
from app.models.donation import Donation
from typing import Union
from app.models.charity_project import CharityProject
from app.crud.charity_project import project_crud
from app.crud.donation import donation_crud
from sqlalchemy.ext.asyncio import AsyncSession


async def obj_close(
    obj: Union[CharityProject, Donation]
) -> Union[CharityProject, Donation]:
    '''Функция закрытия модели!'''
    obj.invested_amount = obj.full_amount
    obj.fully_invested = True
    obj.close_date = datetime.now()
    return obj


async def main_process_invest(
    session: AsyncSession,
    project=None,
    donation=None
) -> Union[CharityProject, Donation]:
    '''Функция инвестирования'''
    #Проверка аргументов, для каждого аргумента свои круд-функции
    if donation:
        crud_func = project_crud
        new_obj = donation
    if project:
        crud_func = donation_crud
        new_obj = project
    #Изходя из аргументов, круд-функция ищет не закрытые обьекты моделей
    get_id_objs_not_closed = await crud_func.get_obj_not_closed(session)
    free_money = new_obj.full_amount - new_obj.invested_amount
    #С помощью цикла перебираем полученые обьекты id
    for id in get_id_objs_not_closed:
        #Получаем по id обьект модели
        get_obj = await crud_func.get(id, session)
        need_amount = get_obj.full_amount - get_obj.invested_amount
        if need_amount > free_money:
            get_obj.invested_amount = get_obj.invested_amount + free_money
            free_money = 0
            new_obj = await obj_close(new_obj)
            session.add(new_obj)
            break
        if need_amount < free_money:
            free_money = 0
            new_obj.invested_amount += need_amount
            get_obj = await obj_close(get_obj)
            session.add(get_obj)
        if need_amount == free_money:
            get_obj.invested_amount = get_obj.invested_amount + free_money
            new_obj.invested_amount = new_obj.invested_amount + need_amount
            free_money = 0
            get_obj = await obj_close(get_obj)
            new_obj = await obj_close(new_obj)
            session.add(new_obj)
            session.add(get_obj)
    #добавляем все наши операции, комитим и перезагружаем базу-данных
    session.add(new_obj)
    await session.commit()
    await session.refresh(new_obj)
    return new_obj
