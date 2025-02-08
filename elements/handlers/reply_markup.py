from aiogram import types, F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from elements.message_builder import (
    start_message,
)


router = Router()


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


@router.message(F.text.lower() == '/ввод')
async def weights_button(message: types.Message):
    """ Вывод сообщения - общей информации."""
    await message.reply('input')


@router.message(F.text.lower() == '/вывод')
async def trading_info_button(message: types.Message):
    """ Вывод сообщения - общей информации."""
    await message.reply('output')
