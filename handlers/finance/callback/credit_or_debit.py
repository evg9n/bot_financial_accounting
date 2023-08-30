from re import sub
from datetime import date, timedelta
from loader import bot
from telebot.types import CallbackQuery
from keyboards.inline.finance import SELECT_DATE_BUTTON, select_date
from work_database.set import set_state_date, set_state, set_state_categore_operation
# from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP
from work_database.get import get_state, get_state_message_id
from utils.calendar import Calendar, LSTEP
from states.finance import *


@bot.callback_query_handler(func=lambda call: (call.data.startswith('categories_credit_') and
                                               get_state(user_id=call.from_user.id) == SELECT_CATEGORIES_FINANCE))
async def select_categore(call: CallbackQuery):
    user_id = call.from_user.id
    categore = sub(pattern='categories_credit_', repl='', string=call.data)
    set_state_categore_operation(user_id=user_id, categore=categore)
    set_state(user_id=user_id, state=DATE_FINANCE)
    await bot.edit_message_text(chat_id=user_id, text='Выбери дату:', message_id=call.message.message_id,
                                reply_markup=select_date())


@bot.callback_query_handler(func=lambda call: (call.data.startswith('select_date_') and
                                               get_state(user_id=call.from_user.id) == DATE_FINANCE))
async def select_date_debit_or_credid(call: CallbackQuery):
    callback = sub('select_date_', '', call.data)
    user_id = call.from_user.id
    message_id = call.message.message_id

    if callback == SELECT_DATE_BUTTON[0]:
        d = date.today()
        set_state_date(user_id=user_id, date=d)
        set_state(user_id=user_id, state=NAME_FINANCE)
        await bot.edit_message_text(text=f"Введите коментарий:",
                                    chat_id=user_id,
                                    message_id=message_id)

    elif callback == SELECT_DATE_BUTTON[1]:
        d = date.today() - timedelta(days=1)
        set_state_date(user_id=user_id, date=d)
        set_state(user_id=user_id, state=NAME_FINANCE)
        await bot.edit_message_text(text=f"Введите коментарий:",
                                    chat_id=user_id,
                                    message_id=message_id)

    elif callback == SELECT_DATE_BUTTON[2]:
        calendar_inline, step = Calendar().build()
        await bot.edit_message_text(chat_id=call.message.chat.id,
                                    text=f'Выбери {LSTEP[step]}:',
                                    reply_markup=calendar_inline,
                                    message_id=call.message.id)


@bot.callback_query_handler(func=lambda call: (Calendar.func() and
                                               get_state(user_id=call.from_user.id) == DATE_FINANCE))
async def calendar(call: CallbackQuery):
    user_id = call.from_user.id
    message_id = call.message.message_id
    result, key, step = Calendar().process(call_data=call.data)

    if not result and key:
        await bot.edit_message_text(text=f"Выбери {LSTEP[step]}:",
                                    chat_id=user_id,
                                    message_id=message_id,
                                    reply_markup=key)
    elif result:
        set_state_date(user_id=user_id, date=result)
        set_state(user_id=user_id, state=NAME_FINANCE)
        await bot.edit_message_text(text=f"Введите коментарий:",
                                    chat_id=user_id,
                                    message_id=message_id)
