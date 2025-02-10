from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types
import datetime

from source.settings.settings import SPLIT_SYM


def income_category_builder() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()

    builder.add(
        types.InlineKeyboardButton(
            text='Зарплата',
            callback_data='category' + SPLIT_SYM + 'Зарплата'
        )
    )
    builder.add(
        types.InlineKeyboardButton(
            text='Купонный доход',
            callback_data='category' + SPLIT_SYM + 'Купонный доход'
        )
    )
    builder.add(
        types.InlineKeyboardButton(
            text='Дивиденты',
            callback_data='category' + SPLIT_SYM + 'Дивиденты'
        )
    )
    builder.add(
        types.InlineKeyboardButton(
            text='Проценты вклада',
            callback_data='category' + SPLIT_SYM + 'Проценты вклада'
        )
    )
    builder.add(
        types.InlineKeyboardButton(
            text='Разовые выплаты',
            callback_data='category' + SPLIT_SYM + 'Разовые выплаты'
        )
    )
    builder.add(
        types.InlineKeyboardButton(
            text='Перевод',
            callback_data='category' + SPLIT_SYM + 'Перевод'
        )
    )
    builder.add(
        types.InlineKeyboardButton(
            text='Другие доходы',
            callback_data='category' + SPLIT_SYM + 'Другие доходы'
        )
    )
    builder.adjust(2)
    return builder


def expenses_category_builder() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()

    builder.add(
        types.InlineKeyboardButton(
            text='ЖКХ',
            callback_data='category' + SPLIT_SYM + 'ЖКХ'
        )
    )
    builder.add(
        types.InlineKeyboardButton(
            text='Интернет',
            callback_data='category' + SPLIT_SYM + 'Интернет'
        )
    )
    builder.add(
        types.InlineKeyboardButton(
            text='Связь',
            callback_data='category' + SPLIT_SYM + 'Связь'
        )
    )
    builder.add(
        types.InlineKeyboardButton(
            text='Подписки',
            callback_data='category' + SPLIT_SYM + 'Подписки'
        )
    )
    builder.add(
        types.InlineKeyboardButton(
            text='Еда',
            callback_data='category' + SPLIT_SYM + 'Еда'
        )
    )
    builder.add(
        types.InlineKeyboardButton(
            text='Хоз. товары',
            callback_data='category' + SPLIT_SYM + 'Хоз. товары'
        )
    )
    builder.add(
        types.InlineKeyboardButton(
            text='Ребенок',
            callback_data='category' + SPLIT_SYM + 'Ребенок'
        )
    )
    builder.add(
        types.InlineKeyboardButton(
            text='Озон/ВБ/Али',
            callback_data='category' + SPLIT_SYM + 'Озон/ВБ/Али'
        )
    )
    builder.add(
        types.InlineKeyboardButton(
            text='Перевод',
            callback_data='category' + SPLIT_SYM + 'Перевод'
        )
    )
    builder.add(
        types.InlineKeyboardButton(
            text='Другие расходы',
            callback_data='category' + SPLIT_SYM + 'Другие расходы'
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


def get_current_date_str():
    current_date = datetime.date.today()
    return f"{current_date.day}.{current_date.month}.{current_date.year}"
