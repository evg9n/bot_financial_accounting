from loader import bot
from keyboards.inline.all_operations import BUTTONS_SELECT_PERIOD, select_period
from re import sub
from telebot.types import CallbackQuery
from datetime import date, timedelta

from states.finance import NAME_TABLE_FINANCE
from utils.plug import plug
from work_database.get import get_state, get_state_date
from work_database.set import set_state_date
from utils.calendar import Calendar, LSTEP


@bot.callback_query_handler(func=lambda call: (call.data.startswith('select_period_operation_') and
                                               get_state(user_id=call.from_user.id) in (NAME_TABLE_FINANCE, )))
async def select_period_operation(call: CallbackQuery):
    """Обработка начала периода"""
    text = sub(pattern='select_period_operation_', repl='', string=call.data)
    user_id = call.from_user.id
    message_id = call.message.message_id

    if text == BUTTONS_SELECT_PERIOD[0]:
        today = date.today()
        set_state_date(user_id=user_id, date=today)
        set_state_date(user_id=user_id, date=today, column_date2=True)
        await plug(user_id=user_id, message_id=message_id, edit=True)

    elif text == BUTTONS_SELECT_PERIOD[1]:
        yesterday = date.today() - timedelta(days=1)
        set_state_date(user_id=user_id, date=yesterday)
        await bot.edit_message_text(chat_id=user_id, text='Выбери окончание периода:', message_id=message_id,
                              reply_markup=select_period(start=False, button_manually=False, button_month=False))

    elif text == BUTTONS_SELECT_PERIOD[2]:
        today = date.today()
        start_month = today - timedelta(days=today.day)
        set_state_date(user_id=user_id, date=start_month)
        set_state_date(user_id=user_id, date=today, column_date2=True)
        await plug(user_id=user_id, message_id=message_id, edit=True)

    elif text == BUTTONS_SELECT_PERIOD[3]:
        calendar_inline, step = Calendar(calendar_id=1).build()
        await bot.edit_message_text(chat_id=user_id, message_id=message_id, text=f'Выбери {LSTEP[step]} начала:',
                                    reply_markup=calendar_inline)


@bot.callback_query_handler(func=lambda call: (call.data.startswith('cbcal_1') and
                                               get_state(user_id=call.from_user.id) in (NAME_TABLE_FINANCE, )))
async def calendar_1(call: CallbackQuery):
    """Обработка календаря ОТ"""
    result, key, step = Calendar(calendar_id=1).process(call_data=call.data)
    user_id = call.from_user.id
    message_id = call.message.message_id

    if not result and key:
        await bot.edit_message_text(text=f"Выбери {LSTEP[step]} начала:",
                                    chat_id=user_id,
                                    message_id=message_id,
                                    reply_markup=key)
    elif result:
        set_state_date(user_id=user_id, date=result)
        await bot.edit_message_text(chat_id=user_id, message_id=message_id,
                                    text="Выбери окончание периода:",
                                    reply_markup=select_period(start=False, button_month=False))


@bot.callback_query_handler(func=lambda call: (call.data.startswith('select_period_2_operation_') and
                                               get_state(user_id=call.from_user.id) in (NAME_TABLE_FINANCE, )))
async def select_period_operation(call: CallbackQuery):
    """Выбор окончание периода"""
    text = sub(pattern='select_period_2_operation_', repl='', string=call.data)
    user_id = call.from_user.id
    message_id = call.message.message_id

    if text == BUTTONS_SELECT_PERIOD[0]:
        today = date.today()
        set_state_date(user_id=user_id, column_date2=True, date=today)
        await plug(user_id=user_id, message_id=message_id, edit=True)

    elif text == BUTTONS_SELECT_PERIOD[1]:
        yesterday = date.today() - timedelta(days=1)
        set_state_date(user_id=user_id, column_date2=True, date=yesterday)
        await plug(user_id=user_id, message_id=message_id, edit=True)

    # elif text == BUTTONS_SELECT_PERIOD[2]:
    #     today = date.today()
    #     start_month = today - timedelta(days=today.day)

    elif text == BUTTONS_SELECT_PERIOD[3]:
        calendar_inline, step = Calendar(calendar_id=2).build()
        await bot.edit_message_text(chat_id=user_id, message_id=message_id, text=f'Выбери {LSTEP[step]} окончание:',
                                    reply_markup=calendar_inline)


@bot.callback_query_handler(func=lambda call: (call.data.startswith('cbcal_2') and
                                               get_state(user_id=call.from_user.id) in (NAME_TABLE_FINANCE, )))
async def calendar_2(call: CallbackQuery):
    """Обработка календаря ДО"""
    user_id = call.from_user.id
    message_id = call.message.message_id
    min_date = get_state_date(user_id=user_id)
    result, key, step = Calendar(calendar_id=2, min_date=min_date).process(call_data=call.data)

    if not result and key:
        await bot.edit_message_text(text=f"Выбери {LSTEP[step]} окончание:",
                                    chat_id=user_id,
                                    message_id=message_id,
                                    reply_markup=key)
    elif result:
        set_state_date(user_id=user_id, date=result, column_date2=True)
        await plug(user_id=user_id, message_id=message_id, edit=True)
