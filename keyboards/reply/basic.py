from telebot.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from work_database.get import get_names_finance


main_menu_buttons = ('Мои финансы', )
BUTTONS_ADD_FINANCE = 'Создать'


def main_menu() -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    buttons = [KeyboardButton(text=button) for button in main_menu_buttons]
    markup.add(*buttons)
    return markup


def list_finance(user_id: int) -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    buttons = list()
    lst = get_names_finance(user_id=user_id)
    for name in lst:
        buttons.append(KeyboardButton(text=name[0]))
    buttons.append(KeyboardButton(text=BUTTONS_ADD_FINANCE))
    markup.add(*buttons)
    return markup
