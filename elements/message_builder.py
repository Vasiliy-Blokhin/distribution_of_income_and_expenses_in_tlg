# Системные сообщения.
def empty_message():
    return '📝 Извините, но файл пустой.'


def empty_output_message():
    return '📝 Извините, но нет результата на ваш запрос.'


def error_message():
    """ Информация об ошибке."""
    return (
        '❗️ Читай внимательнее инструкцию "/информация".'
    )


# Информационные сообщения
def start_message(name):
    """ Стартовое сообщение."""
    hello_message = (
        f'👋Приветсвую, {name}!'
    )
    return hello_message
