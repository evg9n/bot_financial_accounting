from typing import Optional
from loader import bot
from telebot.types import Message
from keyboards.reply import BUTTONS_ADD_FINANCE, main_menu_buttons, list_finance
from work_database.get import get_names_finance, get_state
from work_database.set import set_names_finance, set_state


@bot.message_handler(func=lambda message: get_state(user_id=message.from_user.id) == 'select_finance')
async def select(message: Message):
    if message.text == BUTTONS_ADD_FINANCE:
        set_state(user_id=message.from_user.id, state='create_finance')
        await bot.send_message(chat_id=message.from_user.id, text='Как назовем?(Максимальная длинна 50 символов)')


@bot.message_handler(func=lambda message: get_state(user_id=message.from_user.id) == 'create_finance')
async def create(message: Message):
    name = message.text
    user_id = message.from_user.id
    result = check_name(name=name, user_id=user_id)
    if result is None:
        set_names_finance(user_id=user_id, name=name)
        set_state(user_id=message.from_user.id, state='select_finance')
        await bot.send_message(chat_id=user_id, text='Готово', reply_markup=list_finance(user_id=user_id))
    else:
        text = f'{result}\nПопробуйте другое название'
        await bot.send_message(chat_id=user_id, text=text)


def check_name(name: str, user_id: int) -> Optional[str]:
    list_names_finance = get_names_finance(user_id=user_id)
    list_names_finance = [n[0] for n in list_names_finance]
    if len(name) > 50:
        return ('Превышена максимальное количество символов, максимальная длина символа 50, '
                f'а ваше название {len(name)} символов')
    elif len(name) < 1:
        return 'Вы ничего не прислали'
    elif name == BUTTONS_ADD_FINANCE or name in main_menu_buttons:
        return 'Данное слово не может использоваться в качестве названия'
    elif name in list_names_finance:
        return 'У вас уже есть финансы с таким именем'
    else:
        return
