from loader import bot
from typing import Optional


async def plug(user_id: int, message_id: Optional[int] = None, edit: bool = False):
    text = 'Данная функция в разработке'

    if edit:
        await bot.edit_message_text(chat_id=user_id, message_id=message_id, text=text)
    else:
        await bot.send_message(chat_id=user_id, text=text)
