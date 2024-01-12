from pandas import DataFrame
from io import BytesIO
from matplotlib import pyplot as plt
from re import sub
from datetime import date, timedelta
from telebot.types import CallbackQuery

from loader import bot
from keyboards.inline.report import SELECT_DATE_BUTTON_REPORT, select_date_report_inline
from utils.other import update_date, break_ranks
from work_database.set import set_state_date, set_state
from work_database.get import get_state, get_names_finance_id, get_for_all_report, \
    get_state_name_table, get_state_date, get_for_debit_or_credit_report, get_old_date
from utils.calendar import Calendar, LSTEP
from states.report import *


@bot.callback_query_handler(func=lambda call: (call.data.startswith('menu_data_report') and
                                               get_state(user_id=call.from_user.id) in
                                               (ALL_REPORT, CREDIT_REPORT, )))
async def select_date_report(call: CallbackQuery):
    """Обработка клавиатуры выбора даты ОТ"""
    text = sub(pattern='menu_data_report', repl='', string=call.data)
    user_id = call.from_user.id
    message_id = call.message.message_id

    if text == SELECT_DATE_BUTTON_REPORT[0]:
        today = date.today()
        set_state_date(user_id=user_id, date=today)
        set_state_date(user_id=user_id, date=today, column_date2=True)
        await send_report(user_id=user_id, message_id=message_id)

    elif text == SELECT_DATE_BUTTON_REPORT[1]:
        yesterday = date.today() - timedelta(days=1)
        set_state_date(user_id=user_id, date=yesterday)
        await bot.edit_message_text(chat_id=user_id, text="Выбери до какого периода:", message_id=message_id,
                                    reply_markup=select_date_report_inline(start=False, button_month=False,
                                                                           button_manually=False,
                                                                           button_skip=True))

    elif text == SELECT_DATE_BUTTON_REPORT[2]:
        today = date.today()
        start_month = today - timedelta(days=today.day - 1)
        set_state_date(user_id=user_id, date=start_month)
        set_state_date(user_id=user_id, date=today, column_date2=True)
        await send_report(user_id=user_id, message_id=message_id)

    elif text == SELECT_DATE_BUTTON_REPORT[3]:
        calendar_inline, step = Calendar(calendar_id=1).build()
        await bot.edit_message_text(chat_id=call.message.chat.id,
                                    text=f'Выбери с какого месяца {LSTEP[step]}:',
                                    reply_markup=calendar_inline,
                                    message_id=call.message.id)


@bot.callback_query_handler(func=lambda call: (call.data.startswith('cbcal_1') and
                                               get_state(user_id=call.from_user.id) in
                                               (ALL_REPORT, CREDIT_REPORT, )))
async def calendar_1(call: CallbackQuery):
    """Обработка календаря ОТ"""
    result, key, step = Calendar(calendar_id=1).process(call_data=call.data)
    user_id = call.from_user.id
    message_id = call.message.message_id

    if not result and key:
        await bot.edit_message_text(text=f"Выбери с какого числа {LSTEP[step]}:",
                                    chat_id=user_id,
                                    message_id=message_id,
                                    reply_markup=key)
    elif result:
        set_state_date(user_id=user_id, date=result)
        await bot.edit_message_text(chat_id=user_id, text="Выбери до какого периода:", message_id=message_id,
                                    reply_markup=select_date_report_inline(start=False, button_month=False,
                                                                           button_skip=True))


@bot.callback_query_handler(func=lambda call: (call.data.startswith('menu_data2_report') and
                                               get_state(user_id=call.from_user.id) in
                                               (ALL_REPORT, CREDIT_REPORT, )))
async def select_date2_report(call: CallbackQuery):
    """Обработка клавиатуры выбора даты ДО"""
    text = sub(pattern='menu_data2_report', repl='', string=call.data)
    user_id = call.from_user.id
    message_id = call.message.message_id

    if text == SELECT_DATE_BUTTON_REPORT[0]:
        today = date.today()
        set_state_date(user_id=user_id, date=today, column_date2=True)
        await send_report(user_id=user_id, message_id=message_id)

    elif text == SELECT_DATE_BUTTON_REPORT[1]:
        yesterday = date.today() - timedelta(days=1)
        set_state_date(user_id=user_id, date=yesterday, column_date2=True)
        await send_report(user_id=user_id, message_id=message_id)

    elif text == SELECT_DATE_BUTTON_REPORT[3]:
        min_day = get_state_date(user_id=user_id)
        calendar_inline, step = Calendar(calendar_id=2, min_day=min_day).build()
        await bot.delete_message(chat_id=call.message.chat.id,
                                 message_id=message_id)
        await bot.send_message(chat_id=call.message.chat.id,
                               text=f'Выбери до какого месяца {LSTEP[step]}:',
                               reply_markup=calendar_inline
                               )

    elif text == SELECT_DATE_BUTTON_REPORT[4]:
        date_2 = get_state_date(user_id=user_id)
        set_state_date(user_id=user_id, date=date_2, column_date2=True)
        await send_report(user_id=user_id, message_id=message_id)


@bot.callback_query_handler(func=lambda call: (call.data.startswith('cbcal_2') and
                                               get_state(user_id=call.from_user.id) in
                                               (ALL_REPORT, CREDIT_REPORT, )))
async def calendar_2(call: CallbackQuery):
    """Обработка календаря ДО"""
    user_id = call.from_user.id
    message_id = call.message.message_id
    min_day = get_state_date(user_id=user_id)
    result, key, step = Calendar(calendar_id=2, min_day=min_day).process(call_data=call.data)

    if not result and key:
        await bot.edit_message_text(text=f"Выбери до какого числа {LSTEP[step]}:",
                                    chat_id=user_id,
                                    message_id=message_id,
                                    reply_markup=key)
    elif result:
        set_state_date(user_id=user_id, date=result, column_date2=True)
        await send_report(user_id=user_id, message_id=message_id)


async def send_report(user_id: int, message_id: int):
    """Отправка отчета"""
    state = get_state(user_id=user_id)
    set_state(user_id=user_id, state=TYPE_REPORT)

    # Общий отчет
    if state == ALL_REPORT:
        buf, sum_debit, sum_credit = report_all(user_id=user_id)
        if buf is None:
            await bot.delete_message(chat_id=user_id, message_id=message_id)
            await bot.send_message(chat_id=user_id, text='Нет данных')
        else:
            text = (f'Расход: {break_ranks(sum_credit)}\n'
                    f'Доход: {break_ranks(sum_debit)}\n'
                    f'Прибыль: {break_ranks(sum_debit - sum_credit)}')
            await bot.delete_message(chat_id=user_id, message_id=message_id)
            await bot.send_photo(chat_id=user_id, photo=buf, caption=text)

    # Отчет по расходам
    elif state == CREDIT_REPORT:
        buf, dict_sum = debit_report(user_id=user_id)
        if buf is None:
            await bot.edit_message_text(chat_id=user_id, text='Нет данных', message_id=message_id)
        else:
            text = str()
            s = 0.0
            for key, value in dict_sum.items():
                text += f"{key}: {break_ranks(value)}\n"
                s += value
            else:
                text += f"Всего: {break_ranks(s)}"

            await bot.delete_message(message_id=message_id, chat_id=user_id)
            await bot.send_photo(chat_id=user_id, photo=buf, caption=text)


def report_all(user_id: int):
    """Общий отчет"""
    name_table = get_state_name_table(user_id=user_id)
    id_name_table = get_names_finance_id(user_id=user_id, name=name_table)
    date_1 = get_state_date(user_id=user_id)
    date_2 = get_state_date(user_id=user_id, column_date2=True)
    list_finances_operations = get_for_all_report(user_id=user_id, name_table=id_name_table,
                                                  date_1=date_1, date_2=date_2)
    date_1 = update_date(date_1)
    date_2 = update_date(date_2)

    if list_finances_operations:
        columns = ['сумма', 'доход/расход']

        df = DataFrame(list_finances_operations, columns=columns)
        df['сумма'] = df['сумма'].astype(float)

        # categories = df['доход/расход'].unique()
        sum_credit = float(df.loc[df['доход/расход'] == 'расход', 'сумма'].sum())
        sum_debit = float(df.loc[df['доход/расход'] == 'доход', 'сумма'].sum())
        list_sum = [round(sum_debit, 2), round(sum_credit, 2)]
        exp = (0.1, 0.1)
        plt.pie(x=[sum_debit, sum_credit], labels=['доход', 'расход'], autopct=make_autopct(list_sum),
                colors=['green', 'red'], explode=exp, textprops=dict(fontsize=8))
        plt.title(f'Прибыль: {break_ranks(sum_debit - sum_credit)}\n'
                  f'Период: {date_1} - {date_2}')
        buf = BytesIO()
        plt.savefig(buf, format='png')
        plt.close()
        buf.seek(0)
        return buf, sum_debit, sum_credit

    else:
        return None, None, None


def debit_report(user_id: int):
    """Отчет по расходам"""
    name_table = get_state_name_table(user_id=user_id)
    id_name_table = get_names_finance_id(user_id=user_id, name=name_table)
    date_1 = get_state_date(user_id=user_id)
    date_2 = get_state_date(user_id=user_id, column_date2=True)
    list_finances_operations = get_for_debit_or_credit_report(user_id=user_id, name_table=id_name_table,
                                                              date_1=date_1, date_2=date_2, credit=True)
    date_1 = update_date(date_1)
    date_2 = update_date(date_2)

    if list_finances_operations:

        columns = ['сумма', 'категория']

        df = DataFrame(list_finances_operations, columns=columns)
        df['сумма'] = df['сумма'].astype(float)

        categories = df['категория'].unique()
        dict_sum = dict()
        list_sum = list()
        for categore in categories:
            s = round(float(df.loc[df['категория'] == categore, 'сумма'].sum()), 2)
            dict_sum[categore] = s
            list_sum.append(s)

        plt.pie(x=list_sum, labels=categories, autopct=make_autopct(df['сумма']),
                textprops=dict(fontsize=8))
        plt.title(f'Общий рассход: {break_ranks(sum(list_sum))}\n'
                  f'Период: {date_1} - {date_2}')
        buf = BytesIO()
        plt.savefig(buf, format='png')
        plt.close()
        buf.seek(0)

        return buf, dict_sum

    else:
        return None, None


def make_autopct(values):
    """Вывод суммы на диаграмму"""
    def my_autopct(pct):
        total = sum(values)
        val = float(round(pct * total / 100.0, 2))
        return f'{val}({round(pct, 2)}%)'

    return my_autopct
