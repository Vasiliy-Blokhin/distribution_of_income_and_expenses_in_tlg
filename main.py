""" Основной исполняемый файл (запуск бота). """
import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher

from source.settings.settings import TOKEN
from source.sql.main import SQLmain as sql
from elements import (
    input_router,
    output_router,
    delete_router,
    info_router
)


async def main() -> None:
    """ Выполнение основной части работы бота."""
    bot = Bot(TOKEN,)
    dp = Dispatcher()
    dp.include_routers(
        input_router,
        output_router,
        delete_router,
        info_router
    )
    await dp.start_polling(bot)


if __name__ == '__main__':
    sql.create_all_tables()
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
