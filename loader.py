from telebot.async_telebot import AsyncTeleBot
from telebot.storage import StateMemoryStorage
from constants import Constants

c = Constants()
storage = StateMemoryStorage()
bot = AsyncTeleBot(token=c.BOT_TOKEN, state_storage=storage)
