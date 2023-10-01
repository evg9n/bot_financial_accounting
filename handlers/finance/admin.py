from json import dump, load
from os import remove

from telebot.types import Message

from keyboards.reply.admin import BUTTON_MAILING_ADMIN, mailing_keyboard
from keyboards.reply.basic import main_menu
from loader import bot
from states.admin import TEXT_MAILING_ADMIN, BUTTONS_MAILING_TEXT_ADMIN, PHOTOS_MAILING_ADMIN_STATE, \
    BUTTONS_MAILING_URL_ADMIN
from work_database.get import get_state
from work_database.set import set_state


PATH_JSON = '{user_id}mailing.json'


def set_json(user_id: int, dict_json: dict):
    with open(PATH_JSON.format(user_id=user_id), mode='w', encoding='utf-8') as file:
        dump(dict_json, file, indent=4, ensure_ascii=False)


def get_json(user_id: int):
    with open(PATH_JSON.format(user_id=user_id), mode='r', encoding='utf-8') as file:
        dict_json = load(file)
    return dict_json


def close_mailing(user_id: int) -> str:
    text = 'Рассылка отменена'
    set_state(user_id=user_id)
    try:
        remove(PATH_JSON.format(user_id=user_id))
    except FileNotFoundError:
        pass

    return text


@bot.message_handler(func=lambda message: get_state(message.from_user.id) == TEXT_MAILING_ADMIN)
async def start_text(message: Message):
    user_id = message.from_user.id

    if message.text == BUTTON_MAILING_ADMIN[2]:
        text = close_mailing(user_id)
        await bot.send_message(chat_id=user_id, text=text, reply_markup=main_menu(user_id))

    else:
        text = message.text
        dict_json = dict(text=text, buttons=list(), photos=list())
        set_json(user_id=user_id, dict_json=dict_json)
        set_state(user_id=user_id, state=BUTTONS_MAILING_TEXT_ADMIN)
        text = 'Пришли текст кнопки'
        await bot.send_message(chat_id=user_id, text=text, reply_markup=mailing_keyboard(skip=True))


@bot.message_handler(content_types=['text'],
                     func=lambda message: get_state(message.from_user.id) == BUTTONS_MAILING_TEXT_ADMIN)
async def text_button_mailing(message: Message):
    user_id = message.from_user.id
    text = message.text
    if text == BUTTON_MAILING_ADMIN[2]:
        text = close_mailing(user_id)
        await bot.send_message(chat_id=user_id, text=text, reply_markup=main_menu(user_id))

    elif text == BUTTON_MAILING_ADMIN[1]:
        set_state(user_id=user_id, state=PHOTOS_MAILING_ADMIN_STATE)
        text = 'Пришли фото'
        await bot.send_message(chat_id=user_id, text=text, reply_markup=mailing_keyboard(skip=True))

    else:
        dict_json = get_json(user_id=user_id)
        dict_json['buttons'].append(text)
        set_json(user_id=user_id, dict_json=dict_json)
        set_state(user_id=user_id, state=BUTTONS_MAILING_URL_ADMIN)
        text = 'Пришли ссылку'
        await bot.send_message(chat_id=user_id, text=text, reply_markup=mailing_keyboard())


@bot.message_handler(content_types=['text'],
                     func=lambda message: get_state(message.from_user.id) == BUTTONS_MAILING_URL_ADMIN)
async def text_button_mailing(message: Message):
    user_id = message.from_user.id
    text = message.text

    if text == BUTTON_MAILING_ADMIN[2]:
        text = close_mailing(user_id)
        await bot.send_message(chat_id=user_id, text=text, reply_markup=main_menu(user_id))

    else:
        if text.startswith('https://') or text.startswith('http://'):
            dict_json = get_json(user_id=user_id)
            dict_json['buttons'][-1].append(text)
            set_json(user_id=user_id, dict_json=dict_json)
            set_state(user_id=user_id, state=BUTTONS_MAILING_TEXT_ADMIN)
            text = f'Пришли текст еще одной кнопки или жми {BUTTON_MAILING_ADMIN[1]}'
            await bot.send_message(chat_id=user_id, text=text, reply_markup=mailing_keyboard(skip=True))
        else:
            bot.send_message(chat_id=user_id, text='Разве ссылка так выглядит?🤔', reply_markup=mailing_keyboard())
