from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from keyboards.reply.basic import BUTTON_MAIN_MENU, BUTTONS_BACK


BUTTONS_REPORT_MENU = ('Общий отчет', 'Отчет по расходам', BUTTONS_BACK, BUTTON_MAIN_MENU)


def report_menu() -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(row_width=1)
    buttons = [KeyboardButton(text=text) for text in BUTTONS_REPORT_MENU]
    markup.add(*buttons)
    return markup
