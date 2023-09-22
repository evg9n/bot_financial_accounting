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


def all_operations_inline(current_operations: list, current_sheet: int, max_sheet: int):
    markup = InlineKeyboardMarkup(row_width=3)
    buttons = list()
    callback_data = 'all_operations_inline_'

    buttons.append(InlineKeyboardButton(text="Вид", callback_data=callback_data))
    buttons.append(InlineKeyboardButton(text="Сумма", callback_data=callback_data))
    buttons.append(InlineKeyboardButton(text="Категория", callback_data=callback_data))

    for operation in current_operations:
        callback_data_operation = f'all_operations_inline_{operation[0]}'
        buttons.append(InlineKeyboardButton(text=f"{'🟢' if operation[4] == 'доход' else '🔴'}{operation[4]}",
                                            callback_data=callback_data_operation))
        buttons.append(InlineKeyboardButton(text=str(operation[3]), callback_data=callback_data_operation))

        buttons.append(InlineKeyboardButton(text=operation[5] if operation[5] != 'None' else ' ',
                                            callback_data=callback_data_operation))
    back_button = False if current_sheet == 0 else True
    next_button = False if current_sheet + 1 == max_sheet else True

    buttons.append(InlineKeyboardButton(text="◀️" if back_button else " ",
                                        callback_data=callback_data + "back" if back_button
                                        else callback_data))

    buttons.append(InlineKeyboardButton(text=f"{current_sheet + 1}", callback_data=callback_data))

    buttons.append(InlineKeyboardButton(text="▶️" if next_button else " ",
                                        callback_data=callback_data + "next" if next_button
                                        else callback_data))

    buttons.append(InlineKeyboardButton(text="начало" if back_button else " ",
                                        callback_data=callback_data + "first" if back_button else callback_data))

    buttons.append(InlineKeyboardButton(text=" ", callback_data=callback_data))

    buttons.append(InlineKeyboardButton(text="конец" if next_button else " ",
                                        callback_data=callback_data + "last" if next_button else callback_data))

    buttons.append(InlineKeyboardButton(text="Закрыть❌", callback_data=callback_data + "close"))

    markup.add(*buttons)
    return markup


def operation_inline(id_operation: int) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=1)
    callback_data = 'operation_inline_'

    buttons = [InlineKeyboardButton(text='Назад', callback_data=callback_data + 'back'),
               InlineKeyboardButton(text='Закрыть', callback_data=callback_data + 'close'),
               InlineKeyboardButton(text='Удалить', callback_data=callback_data + f'delete{id_operation}')]

    markup.add(*buttons)
    return markup


def pop_operation_inline(id_operation: int) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=1)
    callback_data = 'delete_operation_'

    buttons = [InlineKeyboardButton(text='Точно 😎', callback_data=callback_data + f'yes{id_operation}'),
               InlineKeyboardButton(text='ОЙ, только не это 😱', callback_data=callback_data + f'no{id_operation}')]

    markup.add(*buttons)
    return markup
