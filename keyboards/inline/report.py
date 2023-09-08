from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


SELECT_DATE_BUTTON_REPORT = ("Сегодня", "Вчера", "За текущий месяц", "Выбрать вручную")


def select_date_report_inline(start: bool) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=1)

    if start:
        buttons = [InlineKeyboardButton(text=text,
                                        callback_data=f'menu_data_report{text}') for text in SELECT_DATE_BUTTON_REPORT]
    else:
        buttons = [InlineKeyboardButton(text=text,
                                        callback_data=f'menu_data2_report{text}') for text in SELECT_DATE_BUTTON_REPORT]

    markup.add(*buttons)
    return markup
