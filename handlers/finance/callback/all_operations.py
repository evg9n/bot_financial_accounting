from loader import bot
from keyboards.inline.all_operations import BUTTONS_SELECT_PERIOD, select_period
from re import sub
from telebot.types import CallbackQuery
from datetime import date, timedelta

from states.finance import NAME_TABLE_FINANCE
from utils.plug import plug
from work_database.get import get_state, get_state_date, get_all_operations, get_state_name_table, get_names_finance_id
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
        # save_all_operation(user_id=user_id, chat_id=call.message.chat.id)
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
    #     start_month = today - timedelta(days=today.day - 1)

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


def save_all_operation(user_id: int, chat_id: int):
    """[(1, 1158909236, 1, Decimal('464646.46'), 'доход', 'None', 'пвапва', datetime.date(2023, 8, 31)),
     (5, 1158909236, 1, Decimal('7484.40'), 'расход', 'Развитие', 'fdsfsdf', datetime.date(2023, 8, 31)),
     (6, 1158909236, 1, Decimal('14564.00'), 'расход', 'Развитие', 'Создать', datetime.date(2023, 9, 1)),
     (7, 1158909236, 1, Decimal('34234.00'), 'расход', 'ЖКХ/Аренда', 'gdfg', datetime.date(2023, 9, 7))]"""
    name_table = get_state_name_table(user_id=user_id)
    name_table = get_names_finance_id(user_id=user_id, name=name_table)
    date_1 = get_state_date(user_id=user_id)
    date_2 = get_state_date(user_id=user_id, column_date2=True)

    list_operations = get_all_operations(user_id=user_id, name_table=name_table, date_1=date_1, date_2=date_2)
    print(list_operations)
    dict_operations = dict()
    step = 2
    first = 0
    number = 1
    for _ in list_operations[::5]:
        print('fdsssssssssssssssssssssssssssssssss')
        dict_operations[number] = list_operations[first:first + step]
        first += step
        number += 1

    print(111111, dict_operations)
    with bot.retrieve_data(user_id=user_id, chat_id=chat_id) as operations:
        ...
