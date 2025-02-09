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
    error_message
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


router = Router()


class InputData(StatesGroup):
    date = State()
    kind = State()
    category = State()
    value = State()


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
            callback_data='date' + SPLIT_SYM + 'today'
        )
    )
    builder.row(
        types.InlineKeyboardButton(
            text='Ввести вручную',
            callback_data='date' + SPLIT_SYM + 'date'
        )
    )
    await message.answer(
        'Выберите ввод даты: ',
        reply_markup=builder.as_markup()
    )


@router.callback_query(F.data.split(SPLIT_SYM)[0] == 'date')
async def create_date(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(InputData.date)
    if callback.data.split(SPLIT_SYM)[1] == 'date':
        await callback.message.answer('Введите дату:')
    else:
        await state.update_data(date=get_current_date_str())
        await callback.message.answer(
            'Выберите тип операции: ',
            reply_markup=kind_builder().as_markup()
        )


@router.message(InputData.date)
async def input_date(message: types.Message, state: FSMContext):
    try:
        if await date_validator(message.text):
            await state.update_data(date=message.text)
        else:
            raise Exception
    except Exception:
        await message.answer(error_message())
        await state.set_state(state=InputData.date)
    await state.update_data(date=message.text)
    # add date validator
    await state.set_state(InputData.kind)
    await message.answer('Выберите тип операции: ', reply_markup=kind_builder().as_markup())


@router.callback_query(F.data.split(SPLIT_SYM)[0] == 'kind')
async def input_income(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(kind=callback.data.split(SPLIT_SYM)[1])
    # add date validator
    await state.set_state(InputData.category)
    if callback.data.split(SPLIT_SYM)[1] == 'Доходы':
        await callback.message.answer(
            'Выберите категорию операции: ',
            reply_markup=income_category_builder().as_markup()
        )
    else:
        await callback.message.answer(
            'Выберите категорию операции: ',
            reply_markup=expenses_category_builder().as_markup()
        )


@router.callback_query(F.data.split(SPLIT_SYM)[0] == 'category')
async def input_category(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(category=callback.data.split(SPLIT_SYM)[1])
    await state.set_state(InputData.value)
    await callback.message.answer('Введите сумму:')


@router.message(InputData.value)
async def input_value(message: types.Message, state: FSMContext):
    try:
        await state.update_data(value=float(message.text))
    except Exception:
        await message.answer(error_message())
        await state.clear()

    data = await state.get_data()
    user_id = message.from_user.id
    date = data['date'].split(SPLIT_SYM)
    in_data = [
        {
            'user_id': user_id,
            'day': int(date[0]),
            'month': int(date[1]),
            'year': int(date[2]),
            'kind': data['kind'],
            'category': data['category'],
            'value': data['value']
        }
    ]
    await message.answer(
        result_input_message(
            date=data['date'],
            name=message.from_user.username,
            category=data['category'],
            value=data['value'],
            kind=data['kind']
        )
    )
    sql.append_data(
        table=MainTable,
        data=in_data
    )
    await state.clear()


# ________________________________________________________________
@router.message(Command('вывод'))
async def output(message: types.Message):
    """ Вывод сообщения - общей информации."""
    await message.reply('output')
