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
    year_instr,
    error_message,
    date_instr,
    value_instr
)
from elements.keyboard import (
    output_date_builder,
    output_kind_builder
)
from elements.module import get_current_date_str, sort_data
from elements.validators import date_validator, year_validator
from source.settings.settings import SPLIT_SYM
from source.sql.main import SQLmain as sql
from source.sql.tables import MainTable


output_router = Router()


class OutputData(StatesGroup):
    date_start = State()
    date_end = State()
    kind = State()
    flag = State()


@output_router.message(Command('вывод'))
async def output(message: types.Message):
    """ Вывод сообщения - общей информации."""
    await message.answer(
        'Выберите период просмотра: ',
        reply_markup=output_date_builder().as_markup()
    )


@output_router.callback_query(F.data.split(SPLIT_SYM)[0] == 'odate')
async def dates_variator(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(OutputData.date_start)
    command = callback.data.split(SPLIT_SYM)
    current_date = get_current_date_str()
    if command[1] == 'За текущий месяц':
        start_date = '01' + SPLIT_SYM + current_date.split(SPLIT_SYM)[1] + SPLIT_SYM + current_date.split(SPLIT_SYM)[2]
        await state.set_state(OutputData.date_end)
        await state.update_data(date_end=current_date)
        await state.set_state(OutputData.kind)
        await callback.message.answer(
            'Введите тип операций:',
            reply_markup=output_kind_builder().as_markup()
        )
    elif command[1] == 'За текущий год':
        start_date = '01' + SPLIT_SYM + '01' + SPLIT_SYM + current_date.split(SPLIT_SYM)[2]
        await state.update_data(date_start=start_date)
        await state.set_state(OutputData.date_end)
        await state.update_data(date_end=current_date)
        await state.set_state(OutputData.kind)
        await callback.message.answer(
            'Введите тип операций:',
            reply_markup=output_kind_builder().as_markup()
        )
    elif command[1] == 'За определенный год':
        await state.set_state(OutputData.flag)
        await state.update_data(flag=1)
        await state.set_state(OutputData.date_start)
        await callback.message.answer('Введите год:')
        await callback.message.answer(year_instr())
    elif command[1] == 'Произвольная дата':
        await state.set_state(OutputData.flag)
        await state.update_data(flag=2)
        await state.set_state(OutputData.date_start)
        await callback.message.answer('Введите стартовую дату:')
        await callback.message.answer(date_instr())


@output_router.message(OutputData.date_start)
async def different_years_and_dates(message: types.Message, state: FSMContext):
    try:
        flag = await state.get_data()
        if flag['flag'] == 1:
            if await year_validator(message.text):
                start_date = '01.01.' + message.text
                end_date = '31.12.' + message.text
            else:
                raise Exception
            await state.update_data(date_start=start_date)
            await state.set_state(OutputData.date_end)
            await state.update_data(date_end=end_date)
            await state.set_state(OutputData.kind)
            await message.answer(
                'Введите тип операций:',
                reply_markup=output_kind_builder().as_markup()
            )
        elif flag['flag'] == 2:
            if await date_validator(message.text):
                await state.update_data(date_start=message.text)
            else:
                raise Exception
            await state.set_state(OutputData.date_end)
            await message.answer('Введите конечную дату:')
            await message.answer(date_instr())
    except Exception:
        await message.answer(error_message())
        await output(message)


@output_router.message(OutputData.date_end)
async def end_date(message: types.Message, state: FSMContext):
    try:
        if await date_validator(message.text):
            await state.update_data(date_end=message.text)
        else:
            raise Exception
        await state.set_state(OutputData.kind)
        await message.answer(
            'Введите тип операций:',
            reply_markup=output_kind_builder().as_markup()
        )
    except Exception:
        await message.answer(error_message())
        await output(message)


@output_router.callback_query(F.data.split(SPLIT_SYM)[0] == 'okind')
async def result(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(kind=callback.data.split(SPLIT_SYM)[1])

    request_data = await state.get_data()
    user_data = sql.get_data_on_user_id(
        table=MainTable,
        user_id=callback.message.from_user.id
    )

    await callback.message.answer(
        len(sort_data(request_data, user_data))
    )
