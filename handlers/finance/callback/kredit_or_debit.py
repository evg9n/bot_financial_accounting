from re import sub
from datetime import date, timedelta
from loader import bot
from telebot.types import CallbackQuery
from keyboards.inline.finance import SELECT_DATE_BUTTON
from work_database.set import set_state_date
import telebot_calendar
from telebot_calendar import CallbackData
from work_database.get import get_state
from states.finance import *


@bot.callback_query_handler(func=lambda call: call.data.startswith('select_date_'))
async def debit_or_credid(call: CallbackQuery):
    callback = sub('select_date_', '', call.data)
    user_id = call.from_user.id

    if callback == SELECT_DATE_BUTTON[0]:
        d = date.today()
        print(1111111111111111111, type(d))
        set_state_date(user_id=user_id, date=d)

    elif callback == SELECT_DATE_BUTTON[1]:
        d = date.today() - timedelta(days=1)
        set_state_date(user_id=user_id, date=d)

    elif callback == SELECT_DATE_BUTTON[2]:
        ...
