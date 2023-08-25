from loader import bot
from telebot.types import Message
from logging import getLogger
from work_database.set import set_users, set_state
from work_database.get import get_state
from work_database.create import create_state_user
from keyboards.reply import main_menu, main_menu_buttons, list_finance


log = getLogger('handler_basic')


@bot.message_handler(commands=['start'])
async def start(message: Message):
    text = 'Дратути'
    set_users(message=message)
    create_state_user(user_id=message.from_user.id)
    await bot.send_message(chat_id=message.from_user.id, text=text, reply_markup=main_menu())


@bot.message_handler(func=lambda message: (message.text == main_menu_buttons[0]) and
                                          (get_state(message.from_user.id) == 'none'))
async def my_finance(message: Message):
    user_id = message.from_user.id
    set_state(user_id=user_id, state='select_finance')
    await bot.send_message(chat_id=message.from_user.id, text='PASS', reply_markup=list_finance(user_id=user_id))
