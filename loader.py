from telebot import TeleBot
from telebot.storage import StateMemoryStorage
from dotenv import load_dotenv
from os import path, environ

load_dotenv(dotenv_path=path.abspath('.env'))

storage = StateMemoryStorage()
TOKEN = environ.get('TOKEN')
bot = TeleBot(token=TOKEN, state_storage=storage)
