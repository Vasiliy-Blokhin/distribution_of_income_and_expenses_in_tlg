import os

from aiogram import types, F, Router
from aiogram.filters import CommandStart
from aiogram.filters import Command
from aiogram.types import FSInputFile
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import datetime

from elements.message_builder import (
    data_card,
    error_message,
    date_instr,
    statistic_message
)
from elements.keyboard import (
    change_builder,
    change_types_builder,
    income_category_builder,
    expenses_category_builder

)
from elements.module import get_current_date_str, sort_data, generate_xlsx
from elements.validators import date_validator, year_validator, id_validator
from source.settings.settings import SPLIT_SYM, BASE_DIR
from source.sql.main import SQLmain as sql
from source.sql.tables import MainTable


change_router = Router()


class ChangeData(StatesGroup):
    id = State()
    date = State()
    kind = State()
    category = State()
    value = State()
    user_id = State()


@change_router.message(Command('изменить'))
async def output(message: types.Message, state: FSMContext):
    """ Вывод сообщения - общей информации."""
    await state.clear()
    await message.answer(
        (
            '📝 Выберите ID вашей операции:\n'
            '* Указано в эксель таблицах.'
        ),
    )
    await state.set_state(ChangeData.id)


@change_router.message(ChangeData.id)
async def input_date(message: types.Message, state: FSMContext):
    try:
        if await id_validator(int(message.text)):
            await state.update_data(id=message.text)
        else:
            raise Exception

        id = message.text
        table_data = sql.get_data_on_id(table=MainTable, id=id)[0]

        await state.update_data(
            kind=table_data['kind'],
            category=table_data['category'],
            value=table_data['value'],
            date=(
                f"{table_data['day']}."
                f"{table_data['month']}."
                f"{table_data['year']}"
            ),
            user_id=table_data['user_id']
        )
        data = await state.get_data()

        if int(data['user_id']) == int(message.from_user.id):
            await message.answer(data_card(
                id=id,
                date=data['date'],
                kind=data['kind'],
                category=data['category'],
                value=data['value']
            ))
            await message.answer('Выберите:', reply_markup=change_builder().as_markup())

        else:
            raise Exception

    except Exception:
        await message.answer(error_message())


@change_router.callback_query(F.data.split(SPLIT_SYM)[0] == 'change')
async def choose_del_or_change(callback: types.CallbackQuery, state: FSMContext):
    if callback.data.split(SPLIT_SYM)[1] == 'delete':
        data = await state.get_data()
        sql.delete_operation(table=MainTable, id=data['id'])
        await callback.message.answer('🟢 Удалено.')
    elif callback.data.split(SPLIT_SYM)[1] == 'change':
        await callback.message.answer('Выберите:', change_types_builder().as_markup())
        await callback.message.answer('Можно выбирать несколько пунктов, по окончанию подтвердите.')


@change_router.callback_query(F.data.split(SPLIT_SYM)[0] == 'change_types')
async def choose_types(callback: types.CallbackQuery, state: FSMContext):
    if callback.data.split(SPLIT_SYM)[1] == 'date':
        await state.set_state(ChangeData.date)
        await callback.message.answer('📝 Введите дату:')
        await callback.message.answer(date_instr())
    elif callback.data.split(SPLIT_SYM)[1] == 'category':
        await callback.message.answer(
            '📝 Выберите категорию операции: ',
            reply_markup=income_category_builder().as_markup()
        )