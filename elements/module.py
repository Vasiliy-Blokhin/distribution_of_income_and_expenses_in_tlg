import datetime
from source.settings.settings import SPLIT_SYM


def get_current_date_str():
    current_date = datetime.date.today()
    return f"{current_date.day}.{current_date.month}.{current_date.year}"


def str_to_date(date_str):
    try:
        day, month, year = date_str.split('.')
        return datetime.date(int(year), int(month), int(day))
    except ValueError:
        return "Неверная дата"


def sort_data(request_data, user_data, callback):
    start_date = str_to_date(request_data['date_start'])
    end_date = str_to_date(request_data['date_end'])
    sort_data = []

    for el in user_data:
        user_date = str_to_date(
            date_str=(
                f"{str(el['day'])}{SPLIT_SYM}"
                f"{str(el['month'])}{SPLIT_SYM}{str(el['year'])}"
            )
        )
        callback.message.answer(
            f"{type(user_data)} - {type(start_date)} - {type(end_date)}\n"
            f"{(user_data)} - {(start_date)} - {(end_date)}\n"
        )
        if user_date >= start_date and user_data <= end_date:
            if request_data['kind'] == 'Доходы' and el['kind'] == 'Доходы':
                sort_data.append(el)
            elif request_data['kind'] == 'Расходы' and el['kind'] == 'Расходы':
                sort_data.append(el)
            else:
                sort_data.append(el)

    return sort_data
