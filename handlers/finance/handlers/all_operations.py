from loader import bot
from keyboards.reply.finance import BUTTONS_MENU_FINANCE
from keyboards.inline.all_operations import select_period

from telebot.types import Message


@bot.message_handler(func=lambda message: message.text == BUTTONS_MENU_FINANCE[3])
async def all_operations(message: Message):
    user_id = message.from_user.id
    await bot.send_message(chat_id=user_id, text='Выбери с какого периода вывести операции:',
                           reply_markup=select_period())
