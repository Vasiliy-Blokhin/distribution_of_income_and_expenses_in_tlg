from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types

from source.settings.settings import (
    SPLIT_SYM,
    CATEGORY_EXPENSES_DICT,
    CATEGORY_INCOME_DICT
)


def income_category_builder(callback) -> InlineKeyboardBuilder:
    if callback is None:
        callback = 'category'
    builder = InlineKeyboardBuilder()
    for key in CATEGORY_INCOME_DICT.keys():
        builder.add(
            types.InlineKeyboardButton(
                text=key,
                callback_data=callback + SPLIT_SYM + key
            )
        )
    builder.adjust(2)
    return builder


def expenses_category_builder(callback) -> InlineKeyboardBuilder:
    if callback is None:
        callback = 'category'
    builder = InlineKeyboardBuilder()
    for key in CATEGORY_EXPENSES_DICT.keys():
        builder.add(
            types.InlineKeyboardButton(
                text=key,
                callback_data=callback + SPLIT_SYM + key
            )
        )
    builder.adjust(2)
    return builder


def kind_builder() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()

    builder.row(
        types.InlineKeyboardButton(
            text='Доходы',
            callback_data='ikind' + SPLIT_SYM + 'Доходы'
        )
    )
    builder.row(
        types.InlineKeyboardButton(
            text='Расходы',
            callback_data='ikind' + SPLIT_SYM + 'Расходы'
        )
    )
    return builder


def output_kind_builder() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()

    builder.row(
        types.InlineKeyboardButton(
            text='Доходы',
            callback_data='okind' + SPLIT_SYM + 'Доходы'
        )
    )
    builder.row(
        types.InlineKeyboardButton(
            text='Расходы',
            callback_data='okind' + SPLIT_SYM + 'Расходы'
        )
    )
    builder.row(
        types.InlineKeyboardButton(
            text='Все',
            callback_data='okind' + SPLIT_SYM + 'Все'
        )
    )
    return builder


def input_date_builder():
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
    return builder


def output_date_builder() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()

    builder.row(
        types.InlineKeyboardButton(
            text='За текущий месяц',
            callback_data='odate' + SPLIT_SYM + 'За текущий месяц'
        )
    )
    builder.row(
        types.InlineKeyboardButton(
            text='За текущий год',
            callback_data='odate' + SPLIT_SYM + 'За текущий год'
        )
    )
    builder.row(
        types.InlineKeyboardButton(
            text='За определенный год',
            callback_data='odate' + SPLIT_SYM + 'За определенный год'
        )
    )
    builder.row(
        types.InlineKeyboardButton(
            text='Произвольная дата',
            callback_data='odate' + SPLIT_SYM + 'Произвольная дата'
        )
    )
    builder.adjust(2)
    return builder


def confirm_builder(callback, with_not):
    if with_not is None:
        with_not = True
    if callback is None:
        callback = 'confirm'

    builder = InlineKeyboardBuilder()

    builder.row(
        types.InlineKeyboardButton(
            text='Да',
            callback_data=callback + SPLIT_SYM + 'Да'
        )
    )
    if with_not:
        builder.row(
            types.InlineKeyboardButton(
                text='Нет',
                callback_data=callback + SPLIT_SYM + 'Нет'
            )
        )
    return builder


def info_builder():
    builder = InlineKeyboardBuilder()

    builder.row(
        types.InlineKeyboardButton(
            text='О проекте',
            callback_data='info' + SPLIT_SYM + 'О проекте'
        )
    )
    builder.row(
        types.InlineKeyboardButton(
            text='О себе',
            callback_data='info' + SPLIT_SYM + 'О себе'
        )
    )
    builder.row(
        types.InlineKeyboardButton(
            text='Поддержать',
            callback_data='info' + SPLIT_SYM + 'Поддержать'
        )
    )
    builder.row(
        types.InlineKeyboardButton(
            text='Отправить сообщение автору',
            callback_data='info' + SPLIT_SYM + 'Отправить сообщение автору'
        )
    )
    return builder


def change_builder():
    builder = InlineKeyboardBuilder()

    builder.row(
        types.InlineKeyboardButton(
            text='Изменить данные',
            callback_data='change' + SPLIT_SYM + 'change'
        )
    )
    builder.row(
        types.InlineKeyboardButton(
            text='Удалить данные',
            callback_data='change' + SPLIT_SYM + 'delete'
        )
    )
    return builder


def change_types_builder():
    builder = InlineKeyboardBuilder()

    builder.row(
        types.InlineKeyboardButton(
            text='Дата',
            callback_data='change_types' + SPLIT_SYM + 'date'
        )
    )
    builder.row(
        types.InlineKeyboardButton(
            text='Категория',
            callback_data='change_types' + SPLIT_SYM + 'category'
        )
    )
    builder.row(
        types.InlineKeyboardButton(
            text='Сумма',
            callback_data='change_types' + SPLIT_SYM + 'value'
        )
    )
    return builder
