from json import dump, load
from os import remove

from telebot.types import Message
from telebot.asyncio_helper import ApiTelegramException

from keyboards.inline.admin import inline_mailing
from keyboards.reply.admin import BUTTON_MAILING_ADMIN, mailing_keyboard
from keyboards.reply.basic import main_menu
from loader import bot
from states.admin import TEXT_MAILING_ADMIN, BUTTONS_MAILING_TEXT_ADMIN, PHOTOS_MAILING_ADMIN_STATE, \
    BUTTONS_MAILING_URL_ADMIN, SEND_MAILING_ADMIN
from work_database.get import get_state, get_users
from work_database.set import set_state, pop_user

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
        dict_json['buttons'].append([text])
        set_json(user_id=user_id, dict_json=dict_json)
        set_state(user_id=user_id, state=BUTTONS_MAILING_URL_ADMIN)
        text = 'Пришли ссылку'
        await bot.send_message(chat_id=user_id, text=text, reply_markup=mailing_keyboard())


@bot.message_handler(content_types=['text'],
                     func=lambda message: get_state(message.from_user.id) == BUTTONS_MAILING_URL_ADMIN)
async def url_button_mailing(message: Message):
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
            text = f'Пришли текст еще одной кнопки или жми "{BUTTON_MAILING_ADMIN[1]}"'
            await bot.send_message(chat_id=user_id, text=text, reply_markup=mailing_keyboard(skip=True))
        else:
            await bot.send_message(chat_id=user_id, text='Разве ссылка так выглядит?🤔', reply_markup=mailing_keyboard())


@bot.message_handler(content_types=['photo'],
                     func=lambda message: get_state(message.from_user.id) == PHOTOS_MAILING_ADMIN_STATE)
async def photos_mailing(message: Message):
    user_id = message.from_user.id
    dict_json = get_json(user_id=user_id)
    dict_json['photos'].append(message.photo[-1].file_id)
    set_json(user_id=user_id, dict_json=dict_json)
    text = f'Пришли еще одну или жми "{BUTTON_MAILING_ADMIN[1]}"'
    await bot.send_message(chat_id=user_id, text=text, reply_markup=mailing_keyboard(skip=True))


@bot.message_handler(content_types=['text'],
                     func=lambda message: get_state(message.from_user.id) == PHOTOS_MAILING_ADMIN_STATE)
async def photos_mailing(message: Message):
    user_id = message.from_user.id
    text = message.text
    if text == BUTTON_MAILING_ADMIN[2]:
        text = close_mailing(user_id)
        await bot.send_message(chat_id=user_id, text=text, reply_markup=main_menu(user_id))

    elif text == BUTTON_MAILING_ADMIN[1]:
        set_state(user_id=user_id, state=SEND_MAILING_ADMIN)
        text = f'После нажатия "{BUTTON_MAILING_ADMIN[0]}" рассылка сразу же уйдет'
        await bot.send_message(chat_id=user_id, text=text, reply_markup=mailing_keyboard(confirm=True))

    else:
        text = f'Что-что? Я не понял'
        await bot.send_message(chat_id=user_id, text=text, reply_markup=mailing_keyboard(skip=True))


@bot.message_handler(content_types=['text'],
                     func=lambda message: get_state(message.from_user.id) == SEND_MAILING_ADMIN)
async def send_mailing(message: Message):
    user_id = message.from_user.id
    text = message.text

    if text == BUTTON_MAILING_ADMIN[0]:
        list_users = get_users(only_user_id=True)
        dict_json = get_json(user_id=user_id)
        text = dict_json.get('text')
        buttons = dict_json.get('buttons')
        photos = dict_json.get('photos')

        for user in list_users:
            try:
                for photo in photos:
                    await bot.send_photo(chat_id=user, photo=photo)
                await bot.send_message(chat_id=user, text=text, reply_markup=inline_mailing(list_buttons=buttons))
            except ApiTelegramException as error:
                if 'Forbidden: bot was blocked by the user' == error.description:
                    pop_user(user_id=user)
                    from loader import environ
                    admins = environ.get('ADMINS')
                    for admin in [int(admin.strip()) for admin in admins.split(',')]:
                        text = f'Пользоватьель {user} заблокировал меня поэтому я его удалил и все его данные😡'
                        await bot.send_message(chat_id=admin, text=text)

        text = 'Рассылка выполнена'
        close_mailing(user_id=user_id)
        await bot.send_message(chat_id=user_id, text=text, reply_markup=main_menu(user_id))

    elif text == BUTTON_MAILING_ADMIN[2]:
        text = close_mailing(user_id)
        await bot.send_message(chat_id=user_id, text=text, reply_markup=main_menu(user_id))

    else:
        text = f'Что-то? Я не понял'
        await bot.send_message(chat_id=user_id, text=text, reply_markup=mailing_keyboard(confirm=True))
