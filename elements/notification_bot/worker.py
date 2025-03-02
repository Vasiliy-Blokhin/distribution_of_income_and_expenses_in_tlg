import requests

from source.settings.settings import (
    TELEGRAM_URL,
    START_MESSAGE,
)


class Notification():

    @classmethod
    async def send_message(self, text):
        message = START_MESSAGE + text
        url = TELEGRAM_URL + message
        requests.get(url)
