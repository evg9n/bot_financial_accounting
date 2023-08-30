from telebot.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from work_database.get import get_names_finance
from keyboards.reply.basic import BUTTON_MAIN_MENU, BUTTONS_BACK


BUTTONS_ADD_FINANCE = 'Создать'
NOT_FINANCE = '(ПУСТО)'
BUTTONS_MENU_FINANCE = ('Приход⬆️', 'Расход⬇️',
                        'Отчеты📊', 'Все операции',
                        BUTTONS_BACK, BUTTON_MAIN_MENU,
                        'Удалить финанс❌',)


def list_finance(user_id: int) -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    buttons = list()
    lst = get_names_finance(user_id=user_id)
    if not lst:
        lst.append(NOT_FINANCE)
    for name in lst:
        buttons.append(KeyboardButton(text=name))

    buttons.append(KeyboardButton(text=BUTTONS_ADD_FINANCE))
    buttons.append(KeyboardButton(text=BUTTON_MAIN_MENU))

    markup.add(*buttons)
    return markup


def create_finance() -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    buttons = [KeyboardButton(text=text) for text in (BUTTONS_BACK, )]
    markup.add(*buttons)
    return markup


def menu_finance() -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    buttons = [KeyboardButton(text) for text in BUTTONS_MENU_FINANCE]
    markup.add(*buttons)
    return markup


def main_menu_or_back() -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    buttons = [KeyboardButton(text) for text in (BUTTONS_BACK, BUTTON_MAIN_MENU)]
    markup.add(*buttons)
    return markup
