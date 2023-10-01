from telebot.types import KeyboardButton, ReplyKeyboardMarkup


BUTTON_MAILING_ADMIN = ("Еще", "Пропустить", 'Отмена')


def mailing_keyboard(more: bool = False, skip: bool = False) -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    buttons = list()

    if more:
        buttons.append(KeyboardButton(text=BUTTON_MAILING_ADMIN[0]))

    if skip:
        buttons.append(KeyboardButton(text=BUTTON_MAILING_ADMIN[1]))

    buttons.append(KeyboardButton(text=BUTTON_MAILING_ADMIN[2]))

    markup.add(buttons)
    return markup
