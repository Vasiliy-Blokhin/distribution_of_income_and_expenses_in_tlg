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
from elements.keyboard import (
    kind_builder,
    income_category_builder,
    expenses_category_builder,
)
from elements.module import get_current_date_str
from elements.validators import date_validator
from source.settings.settings import SPLIT_SYM
from source.sql.main import SQLmain as sql
from source.sql.tables import MainTable


input_router = Router()


class InputData(StatesGroup):
    date = State()
    kind = State()
    category = State()
    value = State()


@input_router.message(CommandStart())
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
@input_router.message(Command('ввод'))
async def input(message: types.Message):
    """ Вывод сообщения - общей информации."""
    builder = InlineKeyboardBuilder()

    builder.row(
        types.InlineKeyboardButton(
            text='Сегодня',
            callback_data='idate' + SPLIT_SYM + 'today'
        )
    )
    builder.row(
        types.InlineKeyboardButton(
            text='Ввести вручную',
            callback_data='idate' + SPLIT_SYM + 'date'
        )
    )
    await message.answer(
        'Выберите ввод даты: ',
        reply_markup=builder.as_markup()
    )


@input_router.callback_query(F.data.split(SPLIT_SYM)[0] == 'idate')
async def create_date(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(InputData.date)
    if callback.data.split(SPLIT_SYM)[1] == 'date':
        await callback.message.answer('Введите дату:')
        await callback.message.answer(date_instr())
    else:
        await state.update_data(date=get_current_date_str())
        await callback.message.answer(
            'Выберите тип операции: ',
            reply_markup=kind_builder().as_markup()
        )


@input_router.message(InputData.date)
async def input_date(message: types.Message, state: FSMContext):
    try:
        if await date_validator(message.text):
            await state.update_data(date=message.text)
        else:
            raise Exception
        await state.update_data(date=message.text)
        await state.set_state(InputData.kind)
        await message.answer(
            'Выберите тип операции: ',
            reply_markup=kind_builder().as_markup()
        )
    except Exception:
        await message.answer(error_message())
        await state.clear()
        await input(message)


@input_router.callback_query(F.data.split(SPLIT_SYM)[0] == 'ikind')
async def input_income(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(kind=callback.data.split(SPLIT_SYM)[1])
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


@input_router.callback_query(F.data.split(SPLIT_SYM)[0] == 'category')
async def input_category(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(category=callback.data.split(SPLIT_SYM)[1])
    await state.set_state(InputData.value)
    await callback.message.answer('Введите сумму:')
    await callback.message.answer(value_instr())


@input_router.message(InputData.value)
async def input_value(message: types.Message, state: FSMContext):
    try:
        await state.update_data(value=float(message.text))
        builder = InlineKeyboardBuilder()

        builder.row(
            types.InlineKeyboardButton(
                text='Да',
                callback_data='confirm' + SPLIT_SYM + 'Да'
            )
        )
        builder.row(
            types.InlineKeyboardButton(
                text='Нет',
                callback_data='confirm' + SPLIT_SYM + 'Нет'
            )
        )
        data = await state.get_data()
        date = data['date'].split(SPLIT_SYM)
        await message.answer(
            result_input_message(
                date=data['date'],
                category=data['category'],
                value=data['value'],
                kind=data['kind']
            )
        )
        await message.answer('Подтвердите ввод данных:', reply_markup=builder.as_markup())
    except Exception:
        await message.answer(error_message())
        await state.clear()


@input_router.callback_query(F.data.split(SPLIT_SYM)[0] == 'confirm')
async def input_category(callback: types.CallbackQuery, state: FSMContext):
    command = callback.data.split(SPLIT_SYM)[1]
    if command == 'Нет':
        await state.clear()
        await callback.message.answer('Отмена.')
    else:
        data = await state.get_data()
        user_id = callback.message.from_user.id
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
        await callback.message.answer('Данные внесены.')
        sql.append_data(
            table=MainTable,
            data=in_data
        )
        await state.clear()
