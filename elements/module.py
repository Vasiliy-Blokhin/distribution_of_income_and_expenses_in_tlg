import datetime

import xlsxwriter

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


def sort_data(request_data, user_data):
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
        if user_date >= start_date and user_date <= end_date:
            if request_data['kind'] == 'Доходы' and el['kind'] == 'Доходы':
                sort_data.append(el)
            elif request_data['kind'] == 'Расходы' and el['kind'] == 'Расходы':
                sort_data.append(el)
            elif request_data['kind'] == 'Все':
                sort_data.append(el)

    return sort_data


def generate_xlsx(sorted_data, request_data, user_id):
    name = (
        f"{user_id}-{request_data['date_start']}-"
        f"{request_data['date_end']}-{request_data['kind']}"
    )
    workbook = xlsxwriter.Workbook(f'{name}.xlsx')
    worksheet = workbook.add_worksheet()

    row = 0
    col = 0
    worksheet.write_row(row, col, sorted_data[0].keys())

    for row, entry in enumerate(sorted_data, start=1):
        worksheet.write_row(row, col, entry.values())

    workbook.close()
    return workbook
