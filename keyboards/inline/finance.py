from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


CATEGORIES_KREDIT = (
    "Одежда/Обувь", "Развлечение", "Связь/Подписка", "Развитие",
    "Электроника", "Путешествие", "Красота/Здоровье", "ЖКХ/Аренда", 
    "Кредит/Долг/Налог", "Кафе/Ресторан", "Маркетплейс", "Побаловать себя)", 
    "Для дома", "Для животных", "Вредная привычка", "Супермаркет", "Транспорт/Авто", "Работа", 
    "Прочее",
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
