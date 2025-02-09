import datetime

from source.settings.settings import SPLIT_SYM

days_dict = {
    1: 31,
    2: 29,
    3: 31,
    4: 30,
    5: 31,
    6: 30,
    7: 31,
    8: 31,
    9: 30,
    10: 31,
    11: 30,
    12: 31
}


async def date_validator(value):
    try:
        date = value.split(SPLIT_SYM)
        day = int(date[0])
        month = int(date[1])
        year = int(date[2])
        if year < 1970 or year > int(datetime.date.today().year):
            return False
        if not month in days_dict:
            return False
        elif day < 1 and day > days_dict[month]:
            return False
        elif  (
            not (
                (year % 4 == 0 and year % 100 != 0) or year % 400 == 0
            ) and month == 2 and day > 28
        ):
            return False
        return True
    except Exception:
        return False
