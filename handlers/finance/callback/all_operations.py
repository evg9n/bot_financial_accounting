from loader import bot
from keyboards.inline.all_operations import BUTTONS_SELECT_PERIOD
from re import sub
from telebot.types import CallbackQuery
from datetime import date, timedelta


@bot.callback_query_handler(func=lambda call: call.data.startswith('select_period_operation_'))
async def select_period_operation(call: CallbackQuery):
    text = sub(pattern='select_period_operation_', repl='', string=call.data)

    if text == BUTTONS_SELECT_PERIOD[0]:
        today = date.today()

    elif text == BUTTONS_SELECT_PERIOD[1]:
        yesterday = date.today() - timedelta(days=1)

    elif text == BUTTONS_SELECT_PERIOD[2]:
        today = date.today()
        start_month = today - timedelta(days=today.day)

    elif text == BUTTONS_SELECT_PERIOD[3]:
        ...


@bot.callback_query_handler(func=lambda call: call.data.startswith('select_period_2_operation_'))
async def select_period_operation(call: CallbackQuery):
    text = sub(pattern='select_period_2_operation_', repl='', string=call.data)

    if text == BUTTONS_SELECT_PERIOD[0]:
        today = date.today()

    elif text == BUTTONS_SELECT_PERIOD[1]:
        yesterday = date.today() - timedelta(days=1)

    elif text == BUTTONS_SELECT_PERIOD[2]:
        today = date.today()
        start_month = today - timedelta(days=today.day)

    elif text == BUTTONS_SELECT_PERIOD[3]:
        ...
