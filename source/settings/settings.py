from os import getenv
import sys
from aiogram import Dispatcher, Bot
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


# Параметры для вывода сообщений.
PARAMS_ALL = {
    'SECID': 'Код',
    'SHORTNAME': 'Название',
    'UPDATETIME': 'Время последнего обновления',
    'LAST': 'Последняя цена (за акцию)',
    'DATAUPDATE': 'Время последнего обновления базы данных',
    'CURRENCYID': 'Валюта',
    'FILTER_SCORE': 'Значение конечной фильтрации',
    'STATUS_FILTER': 'Статус фильтрации'
}
STATUS_UP = 'вероятность роста'
STATUS_DOWN = 'вероятность падения'
STATUS_MEDIUM = 'среднее значение'

STOP_TRADING = 'торги приостановлены'
RUN_TRADING = 'торги идут'
STATUS_MEDIUM = 'среднее значение'
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

DP = Dispatcher()
BOT = Bot(TOKEN,)
