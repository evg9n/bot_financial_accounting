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


def all_operations_inline(all_operations: dict, current_sheet: int, max_sheet: int):
    markup = InlineKeyboardMarkup(row_width=4)
    buttons = list()
    current_operations = all_operations.get(current_sheet)
    for operation in current_operations:
        callback_data = f'all_operations_inline_{operation[0]}'
        buttons.append(InlineKeyboardButton(text=operation[4], callback_data=callback_data))
        buttons.append(InlineKeyboardButton(text=str(operation[3]), callback_data=callback_data))
        buttons.append(InlineKeyboardButton(text=operation[5] if operation[5] != 'None' else ' ',
                                            callback_data=callback_data))
        buttons.append(InlineKeyboardButton(text=str(operation[7]), callback_data=callback_data))

    markup.add(*buttons)
    return markup
