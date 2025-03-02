from aiogram import types, F, Router
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from elements.message_builder import (
    about_author,
    about_project,
    support_project,
    send_message_author,
    send_message_choose,
    error_message,
    support_BTC,
    support_TON,
    support_USDT
)
from elements.keyboard import info_builder, inform_confirm_builder
from elements.notification_bot.worker import Notification
from source.settings.settings import SPLIT_SYM


info_router = Router()


class InfoData(StatesGroup):
    text = State()


@info_router.message(Command('информация'))
async def info(message: types.Message):
    """ Вывод сообщения - общей информации."""
    await message.answer(
        '📝 Выберите что интересует: ',
        reply_markup=info_builder().as_markup()
    )


@info_router.callback_query(F.data.split(SPLIT_SYM)[0] == 'info')
async def choose_info(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    command = callback.data.split(SPLIT_SYM)[1]
    if command == 'О проекте':
        await callback.message.answer(about_project())
    elif command == 'О себе':
        await callback.message.answer(about_author())
    elif command == 'Поддержать':
        await callback.message.answer('• Кошелек TON:')
        await callback.message.answer(support_TON())
        await callback.message.answer('• Монеты BTC:')
        await callback.message.answer(support_BTC())
        await callback.message.answer('• USDT в TRC20:')
        await callback.message.answer(support_USDT())
        await callback.message.answer(support_project())
    elif command == 'Отправить сообщение автору':
        await state.set_state(InfoData.text)
        await callback.message.answer(send_message_choose())


@info_router.message(InfoData.text)
async def send_text(message: types.Message, state: FSMContext):
    await state.update_data(text=message.text)
    data = await state.get_data()
    text = send_message_author(
        text=data['text'],
        user_id=message.from_user.id,
        username=message.from_user.username,
        name=message.from_user.full_name
    )
    await state.update_data(text=text)
    await message.answer(
        '📊 Отправлять?\n\n' + text,
        reply_markup=inform_confirm_builder().as_markup()
    )


@info_router.callback_query(F.data.split(SPLIT_SYM)[0] == 'infconfirm')
async def confirm_send_message(callback: types.CallbackQuery, state: FSMContext):
    try:
        if callback.data.split(SPLIT_SYM)[1] == 'Да':
            data = await state.get_data()
            await Notification.send_message(
                text=data['text']
            )
            await callback.message.answer('🟢 Отправлено.')
        else:
            await callback.message.answer('🔴 Отменено.')
    except Exception:
        await callback.message.answer(error_message())
        await state.clear()
    finally:
        await state.clear()
