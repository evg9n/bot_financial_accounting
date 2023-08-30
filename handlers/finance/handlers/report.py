from keyboards.reply.basic import main_menu
from keyboards.reply.finance import menu_finance
from loader import bot
from telebot.types import Message
from pandas import DataFrame
from io import BytesIO
from matplotlib import pyplot as plt
from keyboards.reply.report import BUTTONS_REPORT_MENU
from states.finance import NAME_TABLE_FINANCE
from work_database.get import get_state, get_names_finance_id, get_state_name_table, get_all_report
from states.report import *
from work_database.set import set_state


@bot.message_handler(func=lambda message: (message.text in BUTTONS_REPORT_MENU and
                                           get_state(user_id=message.from_user.id) == TYPE_REPORT))
async def menu_report(message: Message):
    user_id = message.from_user.id
    text = message.text

    if text == BUTTONS_REPORT_MENU[-1]:
        set_state(user_id=user_id)
        await bot.send_message(chat_id=user_id, text='Главное меню', reply_markup=main_menu())
    elif text == BUTTONS_REPORT_MENU[-2]:
        set_state(user_id=user_id, state=NAME_TABLE_FINANCE)
        await bot.send_message(chat_id=user_id, text='Выбери:', reply_markup=menu_finance())
    elif message.text == BUTTONS_REPORT_MENU[0]:
        name_table = get_state_name_table(user_id=user_id)
        id_name_table = get_names_finance_id(user_id=user_id, name=name_table)
        list_finances_operations = get_all_report(user_id=user_id, name_table=id_name_table)
        buf, sum_debit, sum_credit = report_all(list_finances_operations=list_finances_operations)
        # await bot.send_message(chat_id=user_id, text='asfsdfsdfsfd')
        await bot.send_photo(chat_id=user_id, photo=buf)


def report_all(list_finances_operations: list):

    columns = ['сумма', 'доход/расход']

    df = DataFrame(list_finances_operations, columns=columns)
    df['сумма'] = df['сумма'].astype(float)

    def make_autopct(values):
        def my_autopct(pct):
            total = sum(values)
            val = float(round(pct * total / 100.0, 2))
            return f'{val}({round(pct, 2)}%)'

        return my_autopct

    categories = ["доход", "расход"]
    sum_credit = float(df.loc[df['доход/расход'] == 'расход', 'сумма'].sum())
    sum_debit = float(df.loc[df['доход/расход'] == 'доход', 'сумма'].sum())
    list_sum = [sum_debit, sum_credit]
    exp = (0.1, 0.1)
    wedges, texts, autotexts = plt.pie(x=[sum_debit, sum_credit], labels=categories, autopct=make_autopct(list_sum),
                                       colors=['green', 'red'], explode=exp, textprops=dict(fontsize=8))
    plt.title(f'Прибыль: {sum_debit - sum_credit}')
    # plt.legend(wedges, categories, loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
    # plt.grid()
    # plt.show()
    buf = BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)

    return buf, sum_debit, sum_credit
