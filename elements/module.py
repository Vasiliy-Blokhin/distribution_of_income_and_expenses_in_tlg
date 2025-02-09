from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types
import datetime

from source.settings.settings import SPLIT_SYM


def income_category_builder() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()

    builder.add(
        types.InlineKeyboardButton(
            text='inc_category1',
            callback_data='category' + SPLIT_SYM + 'category1'
        )
    )
    builder.add(
        types.InlineKeyboardButton(
            text='inc_category2',
            callback_data='category' + SPLIT_SYM + 'category2'
        )
    )
    builder.add(
        types.InlineKeyboardButton(
            text='inc_category3',
            callback_data='category' + SPLIT_SYM + 'category3'
        )
    )
    builder.add(
        types.InlineKeyboardButton(
            text='inc_category4',
            callback_data='category' + SPLIT_SYM + 'category4'
        )
    )
    builder.adjust(2)
    return builder


def expenses_category_builder() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()

    builder.add(
        types.InlineKeyboardButton(
            text='exp_category1',
            callback_data='category' + SPLIT_SYM + 'category1'
        )
    )
    builder.add(
        types.InlineKeyboardButton(
            text='exp_category2',
            callback_data='category' + SPLIT_SYM + 'category2'
        )
    )
    builder.add(
        types.InlineKeyboardButton(
            text='exp_category3',
            callback_data='category' + SPLIT_SYM + 'category3'
        )
    )
    builder.add(
        types.InlineKeyboardButton(
            text='exp_category4',
            callback_data='category' + SPLIT_SYM + 'category4'
        )
    )
    builder.adjust(2)
    return builder


def kind_builder() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()

    builder.row(
        types.InlineKeyboardButton(
            text='income',
            callback_data='kind' + SPLIT_SYM + 'income'
        )
    )
    builder.row(
        types.InlineKeyboardButton(
            text='expenses',
            callback_data='kind' + SPLIT_SYM + 'expenses'
        )
    )
    return builder


async def value_validator(message, state, value):
    try:
        if not isinstance(int(value), int):
            await message.answer(
                'Вы ввели неверные данные. \n'
                'Ознакомтесь с правилами еще раз'
            )
            await state.clear()
            return False
    except Exception:
        await message.answer(
            'Вы ввели неверные данные. \n'
            'Ознакомтесь с правилами еще раз'
        )
        await state.clear()
        return False
    return True
