from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


SELECT_DATE_BUTTON_REPORT = ("Сегодня", "Вчера", "За текущий месяц", "Выбрать вручную", "Пропустить")


def select_date_report_inline(start: bool, button_today: bool = True, button_month: bool = True,
                              button_yesterday: bool = True,
                              button_manually: bool = True,
                              button_skip: bool = False) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=1)

    if start:
        callback_data = "menu_data_report"
    else:
        callback_data = "menu_data2_report"

    buttons = list()

    if button_today:
        b = InlineKeyboardButton(text=SELECT_DATE_BUTTON_REPORT[0],
                                 callback_data=f'{callback_data}{SELECT_DATE_BUTTON_REPORT[0]}')
        buttons.append(b)

    if button_yesterday:
        b = InlineKeyboardButton(text=SELECT_DATE_BUTTON_REPORT[1],
                                 callback_data=f'{callback_data}{SELECT_DATE_BUTTON_REPORT[1]}')
        buttons.append(b)

    if button_month:
        b = InlineKeyboardButton(text=SELECT_DATE_BUTTON_REPORT[2],
                                 callback_data=f'{callback_data}{SELECT_DATE_BUTTON_REPORT[2]}')
        buttons.append(b)

    if button_manually:
        b = InlineKeyboardButton(text=SELECT_DATE_BUTTON_REPORT[3],
                                 callback_data=f'{callback_data}{SELECT_DATE_BUTTON_REPORT[3]}')
        buttons.append(b)

    if button_skip:
        b = InlineKeyboardButton(text=SELECT_DATE_BUTTON_REPORT[4],
                                 callback_data=f'{callback_data}{SELECT_DATE_BUTTON_REPORT[4]}')
        buttons.append(b)

    # buttons = [InlineKeyboardButton(text=text,
    #                                     callback_data=f'{current_date}{text}') for text in SELECT_DATE_BUTTON_REPORT]

    markup.add(*buttons)
    return markup
