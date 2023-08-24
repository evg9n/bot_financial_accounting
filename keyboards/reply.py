from telebot.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton


main_menu_buttons = ('Мои финансы', )


def main_menu():
    markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    buttons = [KeyboardButton(text=button) for button in main_menu_buttons]
    markup.add(*buttons)
    return markup
