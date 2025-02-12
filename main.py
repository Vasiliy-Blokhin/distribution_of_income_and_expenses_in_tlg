""" Основной исполняемый файл (запуск бота). """
import asyncio
import logging
import sys

from aiogram import Bot

from source.settings.settings import TOKEN, handler, DP
from source.sql.main import SQLmain as sql
from elements.input.handler import input_router
from elements.output.handler import output_router

logger = logging.getLogger(name=__name__)  # Запуск логга проекта.
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)


async def main() -> None:
    """ Выполнение основной части работы бота."""
    bot = Bot(TOKEN,)
    DP.include_routers(
        input_router,
        output_router
    )
    await DP.start_polling(bot)


if __name__ == '__main__':
    sql.create_all_tables()
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
