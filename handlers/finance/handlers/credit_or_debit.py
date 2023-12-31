from telebot.types import Message

from handlers.finance.handlers.basic import check_sum
from keyboards.inline.finance import categories_credit, select_date
from keyboards.reply.basic import main_menu
from keyboards.reply.finance import menu_finance, BUTTONS_CREDIT_OR_DEBIT, main_menu_or_back
from keyboards.reply.basic import BUTTON_MAIN_MENU, BUTTONS_BACK
from loader import bot
from states.finance import DEBIT_FINANCE, CREDIT_FINANCE, NAME_TABLE_FINANCE, DATE_FINANCE, NAME_FINANCE, \
    SELECT_CATEGORIES_FINANCE, SELECT_CREDIT_OR_DEBIT
from utils.other import update_date, break_ranks
from utils.plug import random_answer
from work_database.get import get_state, get_names_finance_id, get_state_type_operation
from work_database.set import (set_state, set_state_sum_operation, set_state_message_id,
                               set_state_categories_operation, set_table_finance_operations, set_state_type_operation)
from utils.texts_messages import TEXT_MAIN_MENU, TEXT_INPUT_SUM


@bot.message_handler(func=lambda message: (get_state(user_id=message.from_user.id) in
                                           (DEBIT_FINANCE, CREDIT_FINANCE, SELECT_CREDIT_OR_DEBIT)))
async def sum_debit_or_kredit(message: Message):
    """Обработчик прихода и расхода"""
    user_id = message.from_user.id
    number = message.text

    # Вернуться назад
    if number == BUTTONS_BACK:
        set_state(user_id=user_id, state=NAME_TABLE_FINANCE)
        await bot.send_message(chat_id=user_id, text=number, reply_markup=menu_finance(user_id=user_id))
        return

    # Выйти в главное меню
    elif number == BUTTON_MAIN_MENU:
        set_state(user_id=user_id)
        await bot.send_message(chat_id=user_id, text=number, reply_markup=main_menu(user_id))
        return
    current_state = get_state(user_id=user_id)

    # Проверка ввода с меню финанса
    if current_state == SELECT_CREDIT_OR_DEBIT:
        set_state_message_id(user_id=user_id, message_id=message.message_id)
        # Приход
        if number == BUTTONS_CREDIT_OR_DEBIT[0]:
            set_state(user_id=user_id, state=DATE_FINANCE)
            set_state_type_operation(user_id=user_id, debit=True)
            set_state_categories_operation(user_id=user_id)
            await bot.send_message(chat_id=user_id, text='Когда было?', reply_markup=main_menu_or_back())
            await bot.send_message(chat_id=user_id, text='Выбери дату:', reply_markup=select_date())
        # Расход
        elif number == BUTTONS_CREDIT_OR_DEBIT[1]:
            set_state_type_operation(user_id=user_id)
            set_state(user_id=user_id, state=SELECT_CATEGORIES_FINANCE)
            await bot.send_message(chat_id=user_id, text='Что за расход?', reply_markup=main_menu_or_back())
            await bot.send_message(chat_id=user_id, text='Выбери категорию расхода:', reply_markup=categories_credit())
        else:
            text = await random_answer()
            await bot.send_message(chat_id=user_id, text=text)

    else:
        # Проверка полученной суммы
        number = check_sum(number=number)
        if number is None:
            text = "Не похоже на денежную сумму🤔\nПопробуй пожалуйста другое число😊"
            await bot.send_message(chat_id=user_id, text=text)
        else:
            set_state_message_id(user_id=user_id, message_id=message.message_id)

            if current_state == DEBIT_FINANCE:
                set_state(user_id=user_id, state=DATE_FINANCE)
                set_state_sum_operation(user_id=user_id, sum_operation=number)
                set_state_type_operation(user_id=user_id, debit=True)
                set_state_categories_operation(user_id=user_id)
                await bot.send_message(chat_id=user_id, text='Выбери дату:', reply_markup=select_date())

            elif current_state == CREDIT_FINANCE:
                set_state_sum_operation(user_id=user_id, sum_operation=number)
                set_state_type_operation(user_id=user_id)
                set_state(user_id=user_id, state=SELECT_CATEGORIES_FINANCE)
                await bot.send_message(chat_id=user_id, text='Выбери категорию расхода:', reply_markup=categories_credit())


@bot.message_handler(func=lambda message: get_state(user_id=message.from_user.id) == NAME_FINANCE)
async def name_finance(message: Message):
    text = message.text
    user_id = message.from_user.id

    if text == BUTTON_MAIN_MENU:
        set_state(user_id=user_id)
        await bot.send_message(chat_id=user_id, text=TEXT_MAIN_MENU, reply_markup=main_menu(user_id))
    elif text == BUTTONS_BACK:
        set_state(user_id=user_id, state=DATE_FINANCE)
        await bot.send_message(chat_id=user_id, text=TEXT_INPUT_SUM, reply_markup=select_date())
    else:
        result = get_state(user_id=user_id, get_all=True)
        sum_operation = result[4]
        type_operation = result[5]
        date = result[9]
        categories_operation = result[7]
        id_finance = get_names_finance_id(user_id=user_id, name=result[3])
        set_table_finance_operations(user_id=user_id, name_table=id_finance, sum_operation=sum_operation,
                                     type_operation=type_operation,
                                     date=date, name_operation=text, categories_operation=categories_operation)
        set_state(user_id=user_id, state=NAME_TABLE_FINANCE)

        text_categories_operation = "Категория: {t}\n"
        text = (f'Добавлен {type_operation}:\n\n'
                f'Сумма: {break_ranks(sum_operation)}\n'
                f'Дата: {update_date(d=date)}\n'
                f'{"" if categories_operation == "None" else text_categories_operation.format(t=categories_operation)}'
                f'Комментарий: {text}\n')

        await bot.send_message(chat_id=user_id, text=text)

        await bot.send_message(chat_id=user_id, text='Список финансов:', reply_markup=menu_finance(user_id=user_id))


@bot.message_handler(func=lambda message: (get_state(user_id=message.from_user.id) in
                                           (DATE_FINANCE, NAME_FINANCE, SELECT_CATEGORIES_FINANCE, )))
async def other(message: Message):
    text = message.text
    user_id = message.from_user.id

    if text == BUTTON_MAIN_MENU:
        set_state(user_id=user_id)
        await bot.send_message(chat_id=user_id, text=TEXT_MAIN_MENU, reply_markup=main_menu(user_id))
    elif text == BUTTONS_BACK:
        current_state = get_state(user_id=user_id)

        if current_state in (SELECT_CATEGORIES_FINANCE, DATE_FINANCE, ):
            if current_state == SELECT_CATEGORIES_FINANCE:
                set_state(user_id=user_id, state=CREDIT_FINANCE)
            else:
                type_operation = get_state_type_operation(user_id=user_id)
                set_state(user_id=user_id, state=DEBIT_FINANCE if type_operation == 'доход' else CREDIT_FINANCE)
            await bot.send_message(chat_id=user_id, text=TEXT_INPUT_SUM)
        elif NAME_FINANCE == current_state:
            set_state(user_id=user_id, state=DATE_FINANCE)
            await bot.send_message(chat_id=user_id, text=TEXT_INPUT_SUM, reply_markup=select_date())

    else:
        text = await random_answer()
        await bot.send_message(chat_id=user_id, text=text)
