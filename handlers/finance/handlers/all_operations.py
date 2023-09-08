from loader import bot
from keyboards.reply.finance import BUTTONS_MENU_FINANCE
from keyboards.inline.all_operations import select_period
from utils.texts_messages import TEXT_ALL_OPERATIONS

from telebot.types import Message


@bot.message_handler(func=lambda message: message.text == BUTTONS_MENU_FINANCE[3])
async def all_operations(message: Message):
    user_id = message.from_user.id
    await bot.send_message(chat_id=user_id, text=TEXT_ALL_OPERATIONS,
                           reply_markup=select_period())
