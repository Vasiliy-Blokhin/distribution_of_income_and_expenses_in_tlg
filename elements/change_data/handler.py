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

)
from elements.module import get_current_date_str, sort_data, generate_xlsx
from elements.validators import date_validator, year_validator, id_validator
from source.settings.settings import SPLIT_SYM, BASE_DIR
from source.sql.main import SQLmain as sql
from source.sql.tables import MainTable


change_router = Router()


class DeleteData(StatesGroup):
    id = State()


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
    await state.set_state(DeleteData.id)


@change_router.message(DeleteData.id)
async def input_date(message: types.Message, state: FSMContext):
    try:
        if await id_validator(int(message.text)):
            await state.update_data(id=message.text)
        else:
            raise Exception

        id = message.text
        data = sql.get_data_on_id(table=MainTable, id=id)[0]

        if int(data['user_id']) == int(message.from_user.id):
            date = f"{data['day']}.{data['month']}.{data['year']}"
            await message.answer(data_card(
                id=id,
                date=date,
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
async def confirm_send_message(callback: types.CallbackQuery, state: FSMContext):
    if callback.data.split(SPLIT_SYM)[1] == 'delete':
        data = await state.get_data()
        sql.delete_operation(table=MainTable, id=data['id'])
        callback.message.answer(text='🟢 Удалено.')
