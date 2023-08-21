from loader import bot
from telebot.types import Message


@bot.message_handler(commands='start')
def start(message: Message):
    text = 'Дратути'
    bot.send_message(chat_id=message.from_user.id, text=text)
