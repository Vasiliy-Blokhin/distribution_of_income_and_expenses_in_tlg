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
)


router = Router()


class InputData(StatesGroup):
    date = State()


@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    Стартовый набор команд (сообщений).
    """
    builder = ReplyKeyboardBuilder()
    builder.row(  # Вывод информации о весах.
        types.KeyboardButton(text='/ввод',)
    )
    builder.add(  # Вывод информации о весах.
        types.KeyboardButton(text='/вывод',)
    )
    await message.answer(  # Сообщение старт.
        start_message(message.from_user.first_name),
        reply_markup=builder.as_markup(resize_keyboard=True),
    )

# ________________________________________________________________
@router.message(Command('ввод'))
async def input(message: types.Message):
    """ Вывод сообщения - общей информации."""
    builder = InlineKeyboardBuilder()

    builder.row(
        types.InlineKeyboardButton(
            text='Сегодня',
            callback_data='сегодня'
        )
    )
    builder.row(
        types.InlineKeyboardButton(
            text='Ввести вручную',
            callback_data='дата'
        )
    )
    await message.answer('Выберите: ', reply_markup=builder.as_markup())


@router.callback_query(F.data == 'дата')
async def param_shares_button(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(InputData.date)
    await callback.message.answer('input data:')


@router.message(InputData.date)
async def input_end_value(message: types.Message, state: FSMContext):
    await state.update_data(date=message.text)

    data = await state.get_data()
    message.answer(data['date'])

# ________________________________________________________________
@router.message(F.text.lower() == '/вывод')
async def output(message: types.Message):
    """ Вывод сообщения - общей информации."""
    await message.reply('output')
