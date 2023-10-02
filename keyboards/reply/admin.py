from telebot.types import KeyboardButton, ReplyKeyboardMarkup


BUTTON_MAILING_ADMIN = ("Потвердить", "Дальше", 'Отмена',)


def mailing_keyboard(confirm: bool = False, skip: bool = False) -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    buttons = list()

    if confirm:
        buttons.append(KeyboardButton(text=BUTTON_MAILING_ADMIN[0]))

    if skip:
        buttons.append(KeyboardButton(text=BUTTON_MAILING_ADMIN[1]))

    buttons.append(KeyboardButton(text=BUTTON_MAILING_ADMIN[2]))

    markup.add(*buttons)
    return markup
