from loader import bot
from telebot.types import Message
from logging import getLogger
from work_database import add_users
from keyboards.reply import main_menu


log = getLogger('handler_basic')


@bot.message_handler(commands=['start'])
async def start(message: Message):
    text = 'Дратути'
    add_users(message=message)
    await bot.send_message(chat_id=message.from_user.id, text=text, reply_markup=main_menu())
