from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


BUTTONS_SELECT_PERIOD = ("За сегодня", "Вчера", "За текущий месяц", "Указать вручную", )


def select_period(start: bool = True) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=1)

    callback_data = 'select_period_2_operation_'
    if start:
        callback_data = 'select_period_operation_'

    buttons = [
        InlineKeyboardButton(text=text, callback_data=f'{callback_data}{text}') for text in BUTTONS_SELECT_PERIOD
    ]
    markup.add(*buttons)
    return markup
