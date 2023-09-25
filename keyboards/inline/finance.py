from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


CATEGORIES_KREDIT = (
    "Супермаркет", "Одежда", "Развлечение", "Работа",
    "Связь/Подписка", "Развитие", "Красота/Здоровье", "Транспорт/Авто",
    "ЖКХ/Аренда", "Кредит/Долг", "Побаловать себя)",
    "Вредная привычка", "Прочее",
)

SELECT_DATE_BUTTON = ("Сегодня", "Вчера", "Выбрать вручную")


def categories_credit() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=1)
    buttons = [
        InlineKeyboardButton(text=text, callback_data=f"categories_credit_{text}") for text in CATEGORIES_KREDIT
    ]
    markup.add(*buttons)
    return markup


def select_date() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=1)
    buttons = [InlineKeyboardButton(text=text, callback_data=f'select_date_{text}') for text in SELECT_DATE_BUTTON]
    markup.add(*buttons)
    return markup
