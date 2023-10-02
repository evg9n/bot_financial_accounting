from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


def inline_mailing(list_buttons: list) -> InlineKeyboardMarkup | None:
    if list_buttons:
        markup = InlineKeyboardMarkup(row_width=1)
        buttons = [InlineKeyboardButton(text=button[0], url=button[1]) for button in list_buttons]
        markup.add(*buttons)
        return markup
    else:
        return None
