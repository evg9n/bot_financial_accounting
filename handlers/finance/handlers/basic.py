from re import sub
from typing import Optional
from telebot.types import Message

from keyboards.reply.report import report_menu
from states.finance import *
from loader import bot
from keyboards.reply.basic import main_menu, main_menu_buttons
from keyboards.reply.finance import list_finance, BUTTONS_ADD_FINANCE, NOT_FINANCE, \
    create_finance, menu_finance, BUTTONS_MENU_FINANCE, main_menu_or_back, yes_or_no, BUTTONS_YES_OR_NO, \
    buttons_credit_or_debit, BUTTONS_CREDIT_OR_DEBIT
from keyboards.reply.basic import BUTTON_MAIN_MENU, BUTTONS_BACK
from states.report import TYPE_REPORT
from utils.plug import random_answer
from work_database.get import get_names_finance, get_state, get_state_name_table
from work_database.set import set_names_finance, set_state, set_state_name_table, set_state_sum_operation


@bot.message_handler(func=lambda message: get_state(user_id=message.from_user.id) == SELECT_FINANCE)
async def select(message: Message):
    """
    Обработчик выбора финанса
    """
    current_name_table = get_names_finance(user_id=message.from_user.id)
    user_id = message.from_user.id
    text = message.text

    # Создать финанс
    if text in (BUTTONS_ADD_FINANCE, NOT_FINANCE):
        set_state(user_id=user_id, state=CREATE_FINANCE)
        await bot.send_message(chat_id=message.from_user.id,
                               text='Как назовем?(Максимальная длинна 50 символов)',
                               reply_markup=create_finance()
                               )

    # Выбор финанса
    elif text in current_name_table:
        set_state_name_table(user_id=user_id, name_table=message.text)
        set_state(user_id=user_id, state=NAME_TABLE_FINANCE)
        await bot.send_message(chat_id=user_id, text=text, reply_markup=menu_finance(user_id=user_id))

    # Переход в главное меню
    elif text in (BUTTON_MAIN_MENU, ):
        set_state(user_id=message.from_user.id)
        await bot.send_message(chat_id=message.from_user.id, text=text, reply_markup=main_menu(user_id))

    # Заглушка
    else:
        text = await random_answer()
        await bot.send_message(chat_id=user_id, text=text)


@bot.message_handler(func=lambda message: get_state(user_id=message.from_user.id) == CREATE_FINANCE)
async def create(message: Message):
    """Обработчик создания финанса"""
    name = message.text
    user_id = message.from_user.id

    # назад
    if name in (BUTTONS_BACK, ):
        set_state(user_id=user_id, state=SELECT_FINANCE)
        await bot.send_message(chat_id=user_id, text=name, reply_markup=list_finance(user_id=user_id))
    else:
        # Проверка полученного названия финанса
        result = check_name(name=name, user_id=user_id)
        if result is None:
            # Создание финанса
            set_names_finance(user_id=user_id, name=name)
            set_state(user_id=message.from_user.id, state=SELECT_FINANCE)
            await bot.send_message(chat_id=user_id, text='Готово', reply_markup=list_finance(user_id=user_id))
        else:
            text = f'{result}\nПопробуйте другое название'
            await bot.send_message(chat_id=user_id, text=text)


def check_name(name: str, user_id: int) -> Optional[str]:
    """
    Проверка наиминование финанса при созлание финанса
    :param name: проверяемое имя
    :param user_id: id пользователя
    :return: None если все наиминова валидно, иначе строка с текстом ошибки для пользователя
    """
    list_names_finance = get_names_finance(user_id=user_id)
    list_names_finance = [n[0] for n in list_names_finance]
    if len(name) > 50:
        return ('Превышена максимальное количество символов, максимальная длина символа 50, '
                f'а ваше название {len(name)} символов')
    elif len(name) < 1:
        return 'Вы ничего не прислали'
    elif (name in (BUTTONS_ADD_FINANCE, NOT_FINANCE, BUTTON_MAIN_MENU, BUTTONS_BACK)
          or name in main_menu_buttons):
        return 'Данное слово не может использоваться в качестве названия'
    elif name in list_names_finance:
        return 'У вас уже есть финансы с таким именем'
    else:
        return


@bot.message_handler(func=lambda message: get_state(user_id=message.from_user.id) == NAME_TABLE_FINANCE)
async def name_table_finance(message: Message):
    """Обработчик действий с финансом"""
    text = message.text
    user_id = message.from_user.id

    # Удалить финанс
    if text == BUTTONS_MENU_FINANCE[-1]:
        set_state(user_id=user_id, state=DELETE_FINANCE)
        await bot.send_message(chat_id=user_id, text="Точно удалять? 🫣", reply_markup=yes_or_no())

    # Перейти в главное меню
    elif text == BUTTONS_MENU_FINANCE[-2]:
        set_state(user_id=user_id)
        await bot.send_message(chat_id=user_id, text=text, reply_markup=main_menu(user_id))

    # Вернуться назад
    elif text == BUTTONS_MENU_FINANCE[-3]:
        set_state(user_id=user_id, state=SELECT_FINANCE)
        await bot.send_message(chat_id=user_id, text=text, reply_markup=list_finance(user_id=user_id))

    # Указать приход
    elif text == BUTTONS_MENU_FINANCE[0]:
        text = f'Введите сумму прихода:'
        set_state(user_id=user_id, state=DEBIT_FINANCE)
        await bot.send_message(chat_id=user_id, text=text, reply_markup=main_menu_or_back())

    # Указать расход
    elif text == BUTTONS_MENU_FINANCE[1]:
        text = f'Введите сумму расхода:'
        set_state(user_id=user_id, state=CREDIT_FINANCE)
        await bot.send_message(chat_id=user_id, text=text, reply_markup=main_menu_or_back())

    # Отчеты
    elif text == BUTTONS_MENU_FINANCE[2]:
        set_state(user_id=user_id, state=TYPE_REPORT)
        await bot.send_message(chat_id=user_id, text='Какой вид отчета?', reply_markup=report_menu())

    else:
        text = check_sum(number=text)
        if text is None:
            text = await random_answer()
            await bot.send_message(chat_id=user_id, text=text)
        else:
            set_state(user_id=user_id, state=SELECT_CREDIT_OR_DEBIT)
            set_state_sum_operation(user_id=user_id, sum_operation=text)
            text = f'{BUTTONS_CREDIT_OR_DEBIT[0]} или {BUTTONS_CREDIT_OR_DEBIT[1]}?'
            await bot.send_message(chat_id=user_id, text=text, reply_markup=buttons_credit_or_debit())


@bot.message_handler(func=lambda message: get_state(user_id=message.from_user.id) == DELETE_FINANCE)
async def delete_name_table(message: Message):
    text = message.text
    user_id = message.from_user.id

    if BUTTONS_YES_OR_NO[0] == text:
        current_name_table = get_state_name_table(user_id=user_id)
        if current_name_table is not None:
            set_names_finance(user_id=user_id, name=current_name_table, delete=True)
        set_state(user_id=user_id, state=SELECT_FINANCE)
        await bot.send_message(chat_id=user_id, text=f'"{current_name_table}" удалена 😔',
                               reply_markup=list_finance(user_id=user_id))

    elif BUTTONS_YES_OR_NO[1] == text:
        set_state(user_id=user_id, state=NAME_TABLE_FINANCE)
        await bot.send_message(chat_id=user_id, text=f'Правильно 😁',
                               reply_markup=menu_finance(user_id=user_id))

    else:
        text = await random_answer()
        await bot.send_message(chat_id=user_id, text=text)


def check_sum(number: str) -> Optional[float]:
    """Проверка на валидность числа"""
    number = sub(pattern=',', repl='.', string=number).strip()
    try:
        number = float(number)
        number = round(number, 2)
    except (TypeError, ValueError):
        return
    return number
