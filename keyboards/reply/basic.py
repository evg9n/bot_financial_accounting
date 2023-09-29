from telebot.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton

from utils.other import check_admin
from work_database.get import get_names_finance


main_menu_buttons = ('Мои финансы', "Код учетной записи")
main_menu_buttons_admin = ('Количество пользователей', )
BUTTONS_ADD_FINANCE = 'Создать'
BUTTON_MAIN_MENU = 'Главное меню'
BUTTONS_BACK = 'Назад🔙'


def main_menu(user_id: int) -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    buttons = [KeyboardButton(text=button) for button in main_menu_buttons]
    if check_admin(user_id=user_id):
        for text in main_menu_buttons_admin:
            buttons.append(KeyboardButton(text=text))

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
