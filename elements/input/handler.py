from aiogram import types, F, Router
from aiogram.filters import CommandStart
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.utils.keyboard import ReplyKeyboardBuilder
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
    input_date_builder,
    input_confirm_builder
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
    user_id = State()


@input_router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    Стартовый набор команд (сообщений).
    """
    builder = ReplyKeyboardBuilder()
    builder.row(
        types.KeyboardButton(text='/ввод',)
    )
    builder.add(
        types.KeyboardButton(text='/вывод',)
    )
    builder.add(
        types.KeyboardButton(text='/удалить',)
    )
    await message.answer(  # Сообщение старт.
        start_message(message.from_user.first_name),
        reply_markup=builder.as_markup(resize_keyboard=True),
    )

# ________________________________________________________________
@input_router.message(Command('ввод'))
async def input(message: types.Message):
    """ Вывод сообщения - общей информации."""
    await message.answer(
        '📝 Выберите ввод даты: ',
        reply_markup=input_date_builder().as_markup()
    )


@input_router.callback_query(F.data.split(SPLIT_SYM)[0] == 'idate')
async def create_date(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(InputData.date)
    if callback.data.split(SPLIT_SYM)[1] == 'date':
        await callback.message.answer('📝 Введите дату:')
        await callback.message.answer(date_instr())
    else:
        await state.update_data(date=get_current_date_str())
        await callback.message.answer(
            '📝 Выберите тип операции: ',
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
            '📝 Выберите тип операции: ',
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
            '📝 Выберите категорию операции: ',
            reply_markup=income_category_builder().as_markup()
        )
    else:
        await callback.message.answer(
            '📝 Выберите категорию операции: ',
            reply_markup=expenses_category_builder().as_markup()
        )


@input_router.callback_query(F.data.split(SPLIT_SYM)[0] == 'category')
async def input_category(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(category=callback.data.split(SPLIT_SYM)[1])
    await state.set_state(InputData.value)
    await callback.message.answer('📝 Введите сумму:')
    await callback.message.answer(value_instr())


@input_router.message(InputData.value)
async def input_value(message: types.Message, state: FSMContext):
    try:
        await state.update_data(value=float(message.text))
        data = await state.get_data()
        await message.answer(
            result_input_message(
                user_id=str(message.from_user.id),
                date=data['date'],
                category=data['category'],
                value=data['value'],
                kind=data['kind']
            )
        )
        await message.answer(
            '📈 Подтвердите ввод данных:',
            reply_markup=input_confirm_builder().as_markup()
        )
    except Exception:
        await message.answer(error_message())
        await state.clear()


@input_router.callback_query(F.data.split(SPLIT_SYM)[0] == 'iconfirm')
async def input_confirm(callback: types.CallbackQuery, state: FSMContext):
    command = callback.data.split(SPLIT_SYM)[1]
    if command == 'Нет':
        await state.clear()
        await callback.message.answer('🔴 Отмена.')
    else:
        data = await state.get_data()
        user_id = str(callback.from_user.id)
        date = data['date'].split(SPLIT_SYM)
        in_data = [
            {
                'user_id': str(user_id),
                'day': int(date[0]),
                'month': int(date[1]),
                'year': int(date[2]),
                'kind': str(data['kind']),
                'category': str(data['category']),
                'value': float(data['value'])
            }
        ]
        await callback.message.answer('🟢 Данные внесены.')
        sql.append_data(
            table=MainTable,
            data=in_data
        )
        await state.clear()
