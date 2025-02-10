# Системные сообщения.
def empty_message():
    return '📝 Извините, но файл пустой.'


def empty_output_message():
    return '📝 Извините, но нет результата на ваш запрос.'


def error_message():
    """ Информация об ошибке."""
    return (
        '❗️ Читай внимательнее инструкцию.'
    )


# Информационные сообщения
def start_message(name):
    """ Стартовое сообщение."""
    hello_message = (
        f'👋Приветсвую, {name}!'
    )
    return hello_message


def date_instr():
    return (
        'Ввод даты осуществляется в формате:\n'
        'дд.мм.гггг\n'
        'Например:\n'
        '22.12.2024'
    )


def year_instr():
    return (
        'Ввод года осуществляется в формате:\n'
        'гггг\n'
        'Например:\n'
        '2024'
    )


def value_instr():
    return (
        'Если сумму не целая, то значение вводится через точку.\n'
        'Например:\n'
        '1234.56'
    )


def result_input_message(name, date, kind, category, value):
    return (
        "Результат ввода данных:\n\n"
        f"ID пользователя: {name}\n"
        f"Дата операции: {date}\n"
        f"Тип операции: {kind}\n"
        f"Категория операции: {category}\n"
        f"Сумма: {value}\n"
    )
