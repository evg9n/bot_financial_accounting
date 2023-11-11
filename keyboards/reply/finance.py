from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from work_database.get import get_names_finance, get_state_name_table
from keyboards.reply.basic import BUTTON_MAIN_MENU, BUTTONS_BACK


BUTTONS_ADD_FINANCE = 'Создать'
NOT_FINANCE = '(ПУСТО)'
BUTTONS_MENU_FINANCE = ('Приход⬆️', 'Расход⬇️',
                        'Отчеты📊', 'Все операции',
                        BUTTONS_BACK, BUTTON_MAIN_MENU,
                        'Удалить финанс❌',)
BUTTONS_YES_OR_NO = ('Конечно', 'Ой, нет', )
BUTTONS_CREDIT_OR_DEBIT = ('Приход', 'Расход', BUTTONS_BACK, BUTTON_MAIN_MENU)


def buttons_credit_or_debit() -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    buttons = [KeyboardButton(button) for button in BUTTONS_CREDIT_OR_DEBIT]
    markup.add(*buttons)
    return markup


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


def menu_finance(user_id: int) -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    buttons = [KeyboardButton(text) for text in BUTTONS_MENU_FINANCE]
    name_table = get_state_name_table(user_id=user_id)
    if name_table is not None:
        buttons.insert(0, KeyboardButton(text=name_table))
        buttons.insert(0, KeyboardButton(text='Текущий финанс =>'))
    markup.add(*buttons)
    return markup


def main_menu_or_back() -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    buttons = [KeyboardButton(text) for text in (BUTTONS_BACK, BUTTON_MAIN_MENU)]
    markup.add(*buttons)
    return markup


def yes_or_no() -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(row_width=2)
    buttins = [KeyboardButton(text=text) for text in BUTTONS_YES_OR_NO]
    markup.add(*buttins)
    return markup
