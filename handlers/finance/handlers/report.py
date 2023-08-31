from keyboards.inline.report import select_date_report_inline
from keyboards.reply.basic import main_menu
from keyboards.reply.finance import menu_finance
from loader import bot
from telebot.types import Message
from keyboards.reply.report import BUTTONS_REPORT_MENU
from states.finance import NAME_TABLE_FINANCE
from work_database.get import get_state, get_names_finance_id, get_state_name_table
from states.report import *
from work_database.set import set_state


@bot.message_handler(func=lambda message: (message.text in BUTTONS_REPORT_MENU and
                                           get_state(user_id=message.from_user.id) in
                                           (TYPE_REPORT, ALL_REPORT, CREDIT_REPORT, )))
async def menu_report(message: Message):
    user_id = message.from_user.id
    text = message.text

    if text == BUTTONS_REPORT_MENU[-1]:
        set_state(user_id=user_id)
        await bot.send_message(chat_id=user_id, text='Главное меню', reply_markup=main_menu())
    elif text == BUTTONS_REPORT_MENU[-2]:
        set_state(user_id=user_id, state=NAME_TABLE_FINANCE)
        await bot.send_message(chat_id=user_id, text='Выбери:', reply_markup=menu_finance())
    else:
        # name_table = get_state_name_table(user_id=user_id)
        # id_name_table = get_names_finance_id(user_id=user_id, name=name_table)
        if text == BUTTONS_REPORT_MENU[0]:
            set_state(user_id=user_id, state=ALL_REPORT)

        elif text == BUTTONS_REPORT_MENU[1]:
            set_state(user_id=user_id, state=CREDIT_REPORT)

        await bot.send_message(chat_id=user_id, text='Выбери с какого периода:',
                               reply_markup=select_date_report_inline(start=True))


