from typing import Optional

from loader import bot
from utils.texts_messages import TEXT_PLUG

async def plug(user_id: int, message_id: Optional[int] = None, edit: bool = False):
    """Заглушка"""
    if edit:
        await bot.edit_message_text(chat_id=user_id, message_id=message_id, text=TEXT_PLUG)
    else:
        await bot.send_message(chat_id=user_id, text=TEXT_PLUG)
