import handlers
from loader import bot
from telebot.custom_filters import StateFilter
from telebot.types import BotCommand
from os.path import abspath, join
from logging import config, getLogger, DEBUG, INFO
from work_database import create_database, create_table_users
from asyncio import run, gather


FORMAT = "%(levelname)-4s %(name)s [%(asctime)s] %(message)s [line: %(lineno)d]"
datefmt = '%d.%m.%y %H:%M:%S'

level = DEBUG

log_config = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standart': {
            'format': FORMAT,
            'datefmt': datefmt
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': INFO,
            'formatter': 'standart',
            'stream': 'ext://sys.stdout'
        },
        'file_handler': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'level': level,
            'filename': abspath(join('logs', 'log.log')),
            'encoding': 'utf-8',
            'when': 'D',
            'interval': 1,
            'backupCount': 500,
            'formatter': 'standart'
        }
    },
    'loggers': {
        '': {
            'handlers': ['file_handler', 'console'],
            'level': level
        },
    }
}

config.dictConfig(log_config)
log = getLogger()

# DEFAULT_COMMANDS = (
#     ('start', "Запустить бота"),
#     ('menu', str(back_button[0])),
#     ('help', "Вывести справку"),
#     ('install', str(menu_button[1])),
#     ('current_webhook', str(menu_button[2])),
#     ('track', str(menu_button[0])),
# )


async def main():
    # bot.set_my_commands(
    #     [BotCommand(*i) for i in DEFAULT_COMMANDS]
    # )
    bot.add_custom_filter(StateFilter(bot))
    await gather(bot.infinity_polling())


if __name__ == '__main__':
    if create_database():
        if create_table_users():
            run(main())
        else:
            log.warning('Остановка ищ-за создании таблицы users')
    else:
        log.warning('Остановка из-за создании базы данных')
    log.info('STOP')
