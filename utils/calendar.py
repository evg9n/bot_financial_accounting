from datetime import date
from telegram_bot_calendar import DetailedTelegramCalendar

YEAR = 'y'
MONTH = 'm'
DAY = 'd'
SELECT = "s"
GOTO = "g"
NOTHING = "n"
LSTEP = {'y': 'год', 'm': 'месяц', 'd': 'день'}

STEPS = {MONTH: DAY}


class Calendar(DetailedTelegramCalendar):

    first_step = MONTH
    days_of_week = {
        'ru': ["ПН", "ВТ", "СР", "ЧТ", "ПТ", "СБ", "ВС"],
    }
    months = MONTHS = {
        'ru': ["январь ", "февраль", "март", "апрель", "май", "июнь",
               "июль", "август", "сентябрь", "октябрь", "ноябрь", "декабрь"],
    }

    def __init__(self, calendar_id=0, min_day=None):
        locale = 'ru'
        max_day = date.today()
        if min_day is None:
            min_day = date(year=2023, month=1, day=1)

        super(DetailedTelegramCalendar, self).__init__(calendar_id=calendar_id, locale=locale,
                                                       min_date=min_day, max_date=max_day)
