from telebot.async_telebot import AsyncTeleBot
from telebot.storage import StateMemoryStorage
from dotenv import load_dotenv
from os import path, environ

load_dotenv(dotenv_path=path.abspath('.env'))

storage = StateMemoryStorage()
TOKEN = environ.get('TOKEN')
bot = AsyncTeleBot(token=TOKEN, state_storage=storage)
