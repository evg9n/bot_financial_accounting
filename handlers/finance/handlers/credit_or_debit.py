from telebot.types import Message
from handlers.finance.handlers.basic import check_sum
from keyboards.inline.finance import categories_credit, select_date
from keyboards.reply.basic import main_menu
from keyboards.reply.finance import BUTTONS_BACK, menu_finance, BUTTON_MAIN_MENU
from loader import bot
from states.finance import DEBIT_FINANCE, KREDIT_FINANCE, NAME_TABLE_FINANCE
from work_database.get import get_state
from work_database.set import set_state, set_state_sum_operation, set_state_message_id, set_state_categories_operation


@bot.message_handler(func=lambda message: get_state(user_id=message.from_user.id) in (DEBIT_FINANCE, KREDIT_FINANCE))
async def sum_debit_or_kredit(message: Message):
    """Обработчик прихода и расхода"""
    user_id = message.from_user.id
    number = message.text

    # Вернуться назад
    if number == BUTTONS_BACK:
        set_state(user_id=user_id, state=NAME_TABLE_FINANCE)
        await bot.send_message(chat_id=user_id, text=number, reply_markup=menu_finance())
        return

    # Выйти в главное меню
    elif number == BUTTON_MAIN_MENU:
        set_state(user_id=user_id)
        await bot.send_message(chat_id=user_id, text=number, reply_markup=main_menu())
        return
    current_state = get_state(user_id=user_id)

    # Проверка полученной суммы
    number = check_sum(number=number)
    if number is None:
        text = "Не похоже на денежную сумму🤔\nПопробуй пожалуйста другое число😊"
        await bot.send_message(chat_id=user_id, text=text)
    else:
        set_state_sum_operation(user_id=user_id, sum_operation=number)
        set_state_message_id(user_id=user_id, message_id=message.message_id + 1)

        if current_state == DEBIT_FINANCE:
            set_state_categories_operation(user_id=user_id)
            await bot.send_message(chat_id=user_id, text='Выбери дату:', reply_markup=select_date())

        elif current_state == KREDIT_FINANCE:
            await bot.send_message(chat_id=user_id, text='Выбери категорию расхода:', reply_markup=categories_credit())