from logging import getLogger
from telebot.types import Message

from keyboards.reply.admin import mailing_keyboard
from loader import bot
from states.admin import TEXT_MAILING_ADMIN
from utils.backup_db import backup_db
from utils.other import check_admin
from work_database.set import set_users, set_state, set_state_user
from work_database.get import get_state, get_users
from keyboards.reply.basic import main_menu, main_menu_buttons, main_menu_buttons_admin
from keyboards.reply.finance import list_finance
from utils.texts_messages import TEXT_START, TEXT_MY_FINANCE

log = getLogger('handler_basic')


@bot.message_handler(commands=['start'])
async def start(message: Message):
    set_users(message=message)
    set_state(user_id=message.from_user.id)
    set_state_user(user_id=message.from_user.id)
    await bot.send_message(chat_id=message.from_user.id, text=TEXT_START,
                           reply_markup=main_menu(message.from_user.id))


# @bot.message_handler(func=lambda message: (message.text == main_menu_buttons[0]) and
#                                           (get_state(message.from_user.id) == 'none'))
@bot.message_handler(func=lambda message: get_state(message.from_user.id) == 'none')
async def my_finance(message: Message):
    user_id = message.from_user.id
    text = message.text
    if text == main_menu_buttons[0]:
        set_state(user_id=user_id, state='select_finance')
        await bot.send_message(chat_id=message.from_user.id, text=TEXT_MY_FINANCE,
                               reply_markup=list_finance(user_id=user_id))
        return

    elif text == main_menu_buttons[1]:
        await bot.send_message(chat_id=user_id, text=f'Твой код учетной записи: {user_id}',
                               reply_markup=main_menu(message.from_user.id))
        return

    admin = check_admin(user_id)

    if main_menu_buttons_admin[0] == text and admin:
        list_users = get_users()
        text = f"Количество зарегистрированных пользователей: {len(list_users)}"
        await bot.send_message(chat_id=user_id, text=text,
                               reply_markup=main_menu(message.from_user.id))

    elif main_menu_buttons_admin[1] == text and admin:
        text = 'Пришли текст'
        set_state(user_id=user_id, state=TEXT_MAILING_ADMIN)
        await bot.send_message(chat_id=user_id, text=text, reply_markup=mailing_keyboard())

    elif main_menu_buttons_admin[2] == text and admin:
        reslut_backup = backup_db(user_id=user_id)
        text = 'backup готов' if reslut_backup else 'Что-то пошло не так и backup не выполнен'
        await bot.send_message(chat_id=user_id, text=text)

    else:
        text = "Что-то непонятное ты пишешь🤔"
        await bot.send_message(chat_id=user_id, text=text,
                               reply_markup=main_menu(message.from_user.id))
