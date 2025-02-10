from aiogram import types, F, Router
from aiogram.filters import CommandStart
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import datetime

from elements.message_builder import (
    start_message,
    result_input_message,
    error_message,
    date_instr,
    value_instr
)
from elements.module import (
    output_date_builder,
    get_current_date_str
)
from elements.validators import date_validator
from source.settings.settings import SPLIT_SYM
from source.sql.main import SQLmain as sql
from source.sql.tables import MainTable


output_router = Router()


class OutputData(StatesGroup):
    date_start = State()
    date_end = State()
    kind = State()


@output_router.message(Command('вывод'))
async def output(message: types.Message):
    """ Вывод сообщения - общей информации."""
    await message.answer(
        'Выберите период просмотра: ',
        reply_markup=output_date_builder().as_markup()
    )


@output_router.callback_query(F.data.split(SPLIT_SYM)[0] == 'date')
async def in_month(callback: types.CallbackQuery, state: FSMContext):
    command = callback.data.split(SPLIT_SYM)
    state.set_state(OutputData.date_start)
    current_date = get_current_date_str().split(SPLIT_SYM)
    if command[1] == 'За текущий месяц':
        start_date = '01' + SPLIT_SYM + current_date[1::]
        state.update_data(date_start=start_date)
        state.set_state(OutputData.date_end)
        state.update_data(date_start=current_date)
        callback.answer(f'start - {start_date}\nend - {current_date}')
    elif command[1] == 'За текущий год':
        start_date = '01' + SPLIT_SYM + '01' + SPLIT_SYM + current_date[2]
        state.update_data(date_start=start_date)
        state.set_state(OutputData.date_end)
        state.update_data(date_start=current_date)
        callback.answer(f'start - {start_date}\nend - {current_date}')
