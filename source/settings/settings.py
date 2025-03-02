from os import getenv
import sys

from dotenv import load_dotenv
import logging


# Описание хандлера для логгера.
handler = logging.StreamHandler(sys.stdout)
formater = logging.Formatter(
    '%(name)s, %(funcName)s, %(asctime)s, %(levelname)s - %(message)s.'
)
handler.setFormatter(formater)

load_dotenv()
TOKEN = getenv('BOT_TOKEN')

BASE_DIR = getenv('BASE_DIR')

SPLIT_SYM = '-'

db_connector = getenv('db_connector')
db_login = getenv('db_login')
db_password = getenv('db_password')
db_port = getenv('db_port')
db_name = getenv('db_name')
DB_URL = (
    f'{db_connector}://{db_login}:{db_password}'
    f'@localhost:{db_port}/{db_name}'
)

SPLIT_SYM = '.'

INCOME = '🔴 Расходы'
EXPENSES = '🟢 Доходы'
ALL = '🟡 Все'

CATEGORY_INCOME_DICT = {
    'Зарплата': 0,
    'Купонный доход': 0,
    'Дивиденды': 0,
    'Проценты вклада': 0,
    'Репетиторство': 0,
    'Сделка': 0,
    'Репетиторство': 0,
    'Перевод': 0,
    'Разовая выплата': 0,
    'Другие доходы': 0,
}

CATEGORY_EXPENSES_DICT = {
    'ЖКХ': 0,
    'Интернет': 0,
    'Связь': 0,
    'Подписка': 0,
    'Еда': 0,
    'Хозтовар': 0,
    'Озон/ВБ/Али': 0,
    'Здоровье': 0,
    'Ребенок': 0,
    'Перевод': 0,
    'Сделка': 0,
    'Другие расходы': 0,
}
