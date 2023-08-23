import handlers
from loader import bot
from telebot.custom_filters import StateFilter
from telebot.types import BotCommand

from os import listdir, path


# DEFAULT_COMMANDS = (
#     ('start', "Запустить бота"),
#     ('menu', str(back_button[0])),
#     ('help', "Вывести справку"),
#     ('install', str(menu_button[1])),
#     ('current_webhook', str(menu_button[2])),
#     ('track', str(menu_button[0])),
# )


if __name__ == '__main__':
    bot.add_custom_filter(StateFilter(bot))
    # bot.set_my_commands(
    #     [BotCommand(*i) for i in DEFAULT_COMMANDS]
    # )
    bot.infinity_polling()
