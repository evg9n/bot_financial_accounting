from logging import getLogger
from telebot.types import Message

from loader import bot
from work_database.set import set_users, set_state, set_state_user
from work_database.get import get_state, get_test
from keyboards.reply.basic import main_menu, main_menu_buttons
from keyboards.reply.finance import list_finance
from utils.texts_messages import TEXT_START, TEXT_MY_FINANCE

log = getLogger('handler_basic')


@bot.message_handler(commands=['start'])
async def start(message: Message):
    set_users(message=message)
    set_state(user_id=message.from_user.id)
    set_state_user(user_id=message.from_user.id)
    await bot.send_message(chat_id=message.from_user.id, text=TEXT_START, reply_markup=main_menu())


@bot.message_handler(func=lambda message: (message.text == main_menu_buttons[0]) and
                                          (get_state(message.from_user.id) == 'none'))
async def my_finance(message: Message):
    user_id = message.from_user.id
    set_state(user_id=user_id, state='select_finance')
    await bot.send_message(chat_id=message.from_user.id, text=TEXT_MY_FINANCE, reply_markup=list_finance(user_id=user_id))
