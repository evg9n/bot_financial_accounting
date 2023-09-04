from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


BUTTONS_SELECT_PERIOD = ("За сегодня", "Вчера", "За текущий месяц", "Указать вручную", )


def select_period(start: bool = True, button_today: bool = True, button_yesterday: bool = True,
                  button_month: bool = True, button_manually: bool = True) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=1)

    callback_data = 'select_period_2_operation_'
    if start:
        callback_data = 'select_period_operation_'

    buttons = list()

    if button_today:
        b = InlineKeyboardButton(text=BUTTONS_SELECT_PERIOD[0],
                                 callback_data=f'{callback_data}{BUTTONS_SELECT_PERIOD[0]}')
        buttons.append(b)

    if button_yesterday:
        b = InlineKeyboardButton(text=BUTTONS_SELECT_PERIOD[1],
                                 callback_data=f'{callback_data}{BUTTONS_SELECT_PERIOD[1]}')
        buttons.append(b)

    if button_month:
        b = InlineKeyboardButton(text=BUTTONS_SELECT_PERIOD[2],
                                 callback_data=f'{callback_data}{BUTTONS_SELECT_PERIOD[2]}')
        buttons.append(b)

    if button_manually:
        b = InlineKeyboardButton(text=BUTTONS_SELECT_PERIOD[3],
                                 callback_data=f'{callback_data}{BUTTONS_SELECT_PERIOD[3]}')
        buttons.append(b)

    markup.add(*buttons)
    return markup
