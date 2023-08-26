from re import sub

from states.finance import *
from typing import Optional
from loader import bot
from telebot.types import Message
from keyboards.reply.basic import main_menu, main_menu_buttons
from keyboards.reply.finance import list_finance, BUTTONS_ADD_FINANCE, NOT_FINANCE, BUTTON_MAIN_MENU, BUTTONS_BACK, \
    create_finance, menu_finance, BUTTONS_MENU_FINANCE, main_menu_or_back
from work_database.get import get_names_finance, get_state, get_state_name_table
from work_database.set import set_names_finance, set_state, set_state_name_table, set_state_sum_operation


@bot.message_handler(func=lambda message: get_state(user_id=message.from_user.id) == SELECT_FINANCE)
async def select(message: Message):
    current_name_table = get_names_finance(user_id=message.from_user.id)
    user_id = message.from_user.id
    text = message.text

    if text in (BUTTONS_ADD_FINANCE, NOT_FINANCE):
        set_state(user_id=user_id, state=CREATE_FINANCE)
        await bot.send_message(chat_id=message.from_user.id,
                               text='Как назовем?(Максимальная длинна 50 символов)',
                               reply_markup=create_finance()
                               )
    elif text in current_name_table:
        set_state_name_table(user_id=user_id, name_table=message.text)
        set_state(user_id=user_id, state=NAME_TABLE_FINANCE)
        await bot.send_message(chat_id=user_id, text=text, reply_markup=menu_finance())
    elif text in (BUTTON_MAIN_MENU, ):
        set_state(user_id=message.from_user.id)
        await bot.send_message(chat_id=message.from_user.id, text=text, reply_markup=main_menu())


@bot.message_handler(func=lambda message: get_state(user_id=message.from_user.id) == CREATE_FINANCE)
async def create(message: Message):
    name = message.text
    user_id = message.from_user.id
    if name in (BUTTONS_BACK, ):
        set_state(user_id=user_id, state=SELECT_FINANCE)
        await bot.send_message(chat_id=user_id, text=name, reply_markup=list_finance(user_id=user_id))
    else:
        result = check_name(name=name, user_id=user_id)
        if result is None:
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
    text = message.text
    user_id = message.from_user.id

    if text == BUTTONS_MENU_FINANCE[-1]:
        current_name_table = get_state_name_table(user_id=user_id)
        if current_name_table is not None:
            set_names_finance(user_id=user_id, name=current_name_table, delete=True)
        set_state(user_id=user_id, state=SELECT_FINANCE)
        await bot.send_message(chat_id=user_id, text=text, reply_markup=list_finance(user_id=user_id))

    elif text == BUTTONS_MENU_FINANCE[-2]:
        set_state(user_id=user_id)
        await bot.send_message(chat_id=user_id, text=text, reply_markup=main_menu())

    elif text == BUTTONS_MENU_FINANCE[-3]:
        set_state(user_id=user_id, state=SELECT_FINANCE)
        await bot.send_message(chat_id=user_id, text=text, reply_markup=list_finance(user_id=user_id))

    elif text == BUTTONS_MENU_FINANCE[0]:
        text = f'Введите сумму прихода:'
        set_state(user_id=user_id, state=DEBIT_FINANCE)
        await bot.send_message(chat_id=user_id, text=text, reply_markup=main_menu_or_back())

    elif text == BUTTONS_MENU_FINANCE[1]:
        text = f'Введите сумму расхода:'
        set_state(user_id=user_id, state=KREDIT_FINANCE)
        await bot.send_message(chat_id=user_id, text=text, reply_markup=main_menu_or_back())

    elif text == BUTTONS_MENU_FINANCE[2]:
        ...


@bot.message_handler(func=lambda message: get_state(user_id=message.from_user.id) == DEBIT_FINANCE)
async def sum_debit(message: Message):
    user_id = message.from_user.id
    number = message.text

    if number == BUTTONS_BACK:
        set_state(user_id=user_id, state=NAME_TABLE_FINANCE)
        await bot.send_message(chat_id=user_id, text=number, reply_markup=menu_finance())
        return

    elif number == BUTTON_MAIN_MENU:
        set_state(user_id=user_id)
        await bot.send_message(chat_id=user_id, text=number, reply_markup=main_menu())
        return

    number = check_sum(number=number)
    if number is None:
        text = "Не похоже на денежную сумму🤔\nПопробуй пожалуйста другое число😊"
        await bot.send_message(chat_id=user_id, text=text)
    else:
        set_state_sum_operation(user_id=user_id, sum_operation=number)
        ...


def check_sum(number: str) -> Optional[float]:
    number = sub(pattern=',', repl='.', string=number)
    try:
        number = float(number)
        number = round(number, 2)
    except (TypeError, ValueError):
        return
    return number
