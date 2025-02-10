from aiogram import types, F, Router
from aiogram.filters import CommandStart
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from elements.message_builder import (
    start_message,
    result_input_message,
    error_message,
    date_instr,
    value_instr
)
from elements.module import (
    kind_builder,
    income_category_builder,
    expenses_category_builder,
    get_current_date_str
)
from elements.validators import date_validator
from source.settings.settings import SPLIT_SYM
from source.sql.main import SQLmain as sql
from source.sql.tables import MainTable


output_router = Router()


class OutputData(StatesGroup):
    date = State()
    kind = State()
    category = State()
    value = State()


@output_router.message(Command('вывод'))
async def output(message: types.Message):
    """ Вывод сообщения - общей информации."""
    await message.reply('output')
