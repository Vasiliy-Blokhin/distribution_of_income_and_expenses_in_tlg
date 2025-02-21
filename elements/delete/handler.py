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
    start_message,
    year_instr,
    error_message,
    date_instr,
    statistic_message
)
from elements.keyboard import (
    output_date_builder,
    output_kind_builder,
    output_confirm_builder
)
from elements.module import get_current_date_str, sort_data, generate_xlsx
from elements.validators import date_validator, year_validator, id_validator
from source.settings.settings import SPLIT_SYM, BASE_DIR
from source.sql.main import SQLmain as sql
from source.sql.tables import MainTable


delete_router = Router()


class DeleteData(StatesGroup):
    id = State()


@delete_router.message(Command('удалить'))
async def output(message: types.Message, state: FSMContext):
    """ Вывод сообщения - общей информации."""
    await message.answer(
        (
            '📝 Выберите ID вашей операции:\n'
            '* Указано в эксель таблицах.'
        ),
    )
    await state.set_state(DeleteData.id)


@delete_router.message(DeleteData.id)
async def input_date(message: types.Message, state: FSMContext):
    try:
        if await id_validator(int(message.text)):
            await state.update_data(id=message.text)
        else:
            raise Exception

        id = message.text
        operation = sql.get_data_on_id(
            table=MainTable,
            id=id
        )[0]
        if int(operation['user_id']) == int(message.from_user.id):
            sql.delete_operation(table=MainTable, id=id)
            await message.answer('🟢 Удалено')
        else:
            raise Exception

    except Exception:
        await message.answer(error_message())
