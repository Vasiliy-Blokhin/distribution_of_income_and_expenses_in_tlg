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
        '📊 Ввод даты осуществляется в формате:\n'
        'дд.мм.гггг\n'
        'Например:\n'
        '👉 22.12.2024'
    )


def year_instr():
    return (
        '📊 Ввод года осуществляется в формате:\n'
        'гггг\n'
        'Например:\n'
        '👉 2024'
    )


def value_instr():
    return (
        '📊 Если сумму не целая, то значение вводится через точку.\n'
        'Например:\n'
        '👉 1234.56'
    )


def result_input_message(date, kind, category, value, user_id):
    return (
        "📊 Результат ввода данных:\n\n"
        f"👉 ID пользователя: {user_id}\n"
        f"👉 Дата операции: {date}\n"
        f"👉 Тип операции: {kind}\n"
        f"👉 Категория операции: {category}\n"
        f"👉 Сумма: {value}\n"
    )


def statistic_message(sorted_data, request_data):
    income_value = 0
    expenses_value = 0
    for el in sorted_data:
        if el['kind'] == 'Доходы':
            income_value += el['value']
        elif el['kind'] == 'Расходы':
            expenses_value += el['value']

    if request_data['kind'] == 'Доходы':
        return (
            f"📊 Доходы за период {request_data['date_start']}"
            f" - {request_data['date_end']}: "
            f"{income_value} руб."
        )
    elif request_data['kind'] == 'Расходы':
        return (
            f"📊 Расходы за период {request_data['date_start']}"
            f" - {request_data['date_end']}: "
            f"{expenses_value} руб."
        )
    elif request_data['kind'] == 'Все':
        return (
            f"📊 За период {request_data['date_start']}"
            f" - {request_data['date_end']}:\n\n"
            f"👉 Доходы - {income_value} руб.;\n"
            f"👉 Расходы - {expenses_value} руб.;\n"
            f"👉 Разница - {income_value - expenses_value} руб.;\n"
            f"👉 Соотношение - {100 * (1 - expenses_value/income_value):.2f}%;\n"
        )
