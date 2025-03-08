from source.settings.settings import (
    CATEGORY_INCOME_DICT,
    CATEGORY_EXPENSES_DICT
)


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
        f"👉 Сумма: {value:.2f}\n"
    )


async def statistic_message(sorted_data, request_data):
    income_value = 0
    expenses_value = 0
    income_dict = CATEGORY_INCOME_DICT.copy()
    expenses_dict = CATEGORY_EXPENSES_DICT.copy()

    for el in sorted_data:
        if el['kind'] == 'Доходы':
            income_value += el['value']
        elif el['kind'] == 'Расходы':
            expenses_value += el['value']

    if income_value == 0 and request_data['kind'] == 'Доходы':
        return '🔴 У вас нет зарегистрированных доходов.'
    elif expenses_value == 0 and request_data['kind'] == 'Расходы':
        return '🔴 У вас нет зарегистрированных расходов.'
    elif income_value == 0 and expenses_value == 0:
        return empty_output_message()

    if request_data['kind'] == 'Доходы':
        for el in sorted_data:
            for key, value in income_dict.items():
                if el['category'] == key:
                    value += el['value']
                income_dict[key] = value

        result = (
            f"📊 Доходы за период {request_data['date_start']}"
            f" - {request_data['date_end']}: "
            f"{income_value:.2f} руб.\n\n"
        )
        for key, value in income_dict.items():
            if value:
                result += (
                    f'👉 {key} - {(value):.2f} руб.\n'
                )

        return result

    elif request_data['kind'] == 'Расходы':
        for el in sorted_data:
            for key, value in expenses_dict.items():
                if el['category'] == key:
                    value += el['value']
                expenses_dict[key] = value

        result = (
            f"📊 Расходы за период {request_data['date_start']}"
            f" - {request_data['date_end']}: "
            f'{expenses_value:.2f} руб.\n\n'
        )
        for key, value in expenses_dict.items():
            if value:
                result += (
                    f'👉 {key} - {(value):.2f} руб.\n'
                )

        return result

    elif request_data['kind'] == 'Все':
        return (
            f"📊 За период {request_data['date_start']}"
            f" - {request_data['date_end']}:\n\n"
            f'👉 Доходы - {(income_value):.2f} руб.;\n'
            f'👉 Расходы - {(expenses_value):.2f} руб.;\n'
            f'👉 Разница - {(income_value - expenses_value):.2f} руб.;\n'
            f'👉 Соотношение - {100 * (1 - expenses_value/income_value):.2f}%;\n'
        )


def data_card(id, kind, category, value, date):
    return (
        f'👉 ID - {id}\n'
        f'👉 Дата - {date}\n'
        f'👉 Тип операции - {kind}\n'
        f'👉 Категория - {category}\n'
        f'👉 Сумма - {value} .руб\n'
    )


def about_project():
    return (
        '📊 О проекте:\n\n'
        'Ваша персональная бюджетная книжка\n'
        'Добро пожаловать в систему учета финансов! '
        'Здесь вы можете эффективно управлять своими '
        'денежными потоками и всегда быть в курсе своего '
        'финансового положения.\n\n'
        'Как это работает:\n'
        'Добавление операций:\n'
        '    • Записывайте все свои доходы и расходы\n'
        '    • Каждая операция сохраняется с датой и суммой\n'
        '    • Так же добавляйте категории операциям\n'
        'Аналитика и отчеты:\n'
        '    • Просмотр всех операций за выбранный период\n'
        '    • Отдельные отчеты по доходам и расходам\n'
        '    • Статистика за текущий месяц и год\n'
        '    • Анализ за любой выбранный период\n'
        '    • Годовая отчетность\n'
        'Преимущества использования:\n'
        '    • Простота в освоении\n'
        '    • Быстрый доступ к информации\n'
        '    • Наглядная статистика\n'
        '    • Возможность планирования бюджета\n'
        '    • Вывод сразу в экселе\n'
        '    • Контроль над расходами\n\n'
        'Начните вести учет своих финансов прямо сейчас!\n'
    )


def about_author():
    return (
        '📊 О себе:\n\n'
        '👋 Привет! Я обычный инженер с необычным хобби - в свободное время я '
        'создаю полезные программные проекты.\n\n'

        '🛠 Почему я это делаю?\n'
        '    • Люблю решать интересные задачи\n'
        '    • Хочу делать жизнь людей проще\n'
        '    • Нахожу удовольствие в создании полезных инструментов\n\n'

        '💡 Этот телеграм-бот для учета финансов - один из моих проектов, '
        'который родился из личного желания лучше контролировать свои расходы.'
        '\n\n'

        '🎯 Мои цели:\n'
        '    • Создавать простые и удобные решения\n'
        '    • Делиться полезными инструментами\n'
        '    • Слушать ваше мнение и улучшать проекты\n\n'

        '📢 Хотите предложить идею для нового проекта или дать обратную связь? '
        'Используйте кнопку “Отправить сообщение автору” - ваши мысли могут'
        ' стать следующим полезным инструментом!'
    )


def support_project():
    return (
        '🎯 Ваша поддержка даст мотивацию для дальнейшей работы.\n'
        '📢 Не забывайте делиться своими мыслями и идеями: "Информация" - '
        '“Отправить сообщение автору”'
    )


def support_TON():
    return 'UQD68V3nEXGjaoAK5B9ANCzQdgKhue9e-hXnXlerYUon1Dix'


def support_BTC():
    return '1EZRKGoRJB2AmQnHQKLeD857juYmt2Rrbv'


def support_USDT():
    return 'TLChT93rWmr3gRmJT5ffHRhH1Sy7881D1z'


def send_message_choose():
    return (
        '📝 Напишите сообщение:'
    )


def send_message_author(user_id, username, name, text):
    return (
        f'👉 ID пользователя: {user_id}\n'
        f'👉 Имя пользователя: {username}\n'
        f'👉 Полное имя: {name}\n'
        f'👉 Текст: "{text}"'
    )
