from os import environ, path, listdir, getenv

from dotenv import load_dotenv


class Constants:

    def __init__(self):
        path_env = path.abspath('env')

        try:
            for env in listdir(path_env):
                if env.endswith('.env'):
                    load_dotenv(path.join(path_env, env))
        except FileNotFoundError:
            pass

        # bot
        self.BOT_TOKEN = environ.get('TOKEN')
        assert self.BOT_TOKEN, 'Отсутствует BOT_TOKEN'

        # admins
        self.ADMINS = environ.get('ADMINS', '').split(',')
        if self.ADMINS[0] == '':
            self.ADMINS = []

        # db postgresql
        self.USER_NAME = environ.get('USER_NAME')
        assert self.USER_NAME, 'Отсутствует USER_NAME'

        self.PASSWORD = environ.get('PASSWORD')
        assert self.PASSWORD, 'Отсутствует PASSWORD'

        self.HOST = environ.get('HOST')
        assert self.HOST, 'Отсутствует HOST'

        self.PORT = environ.get('PORT')
        assert self.PORT, 'Отсутствует PORT'
        self.PORT = int(self.PORT)

        self.NAME_DATABASE = environ.get('NAME_DATABASE')
        assert self.NAME_DATABASE, 'Отсутствует NAME_DATABASE'

        # логирование
        self.FORMAT_LOGGER = getenv('FORMAT_LOGGER',
                                    default='{time:YYYY-MM-DD HH:mm:ss} | {level} | {file} | {message}')
        self.LEVEL_FILE_LOGGER = getenv('LEVEL_FILE_LOGGER', default='DEBUG')
        self.LEVEL_CONSOLE_LOGGER = getenv('LEVEL_CONSOLE_LOGGER', default='INFO')
        self.ROTATION_LOGGER = getenv('ROTATION_LOGGER', default='1 day')
        self.SERIALIZE_LOGGER = getenv('SERIALIZE_LOGGER', default=None) == 'True'


def __setattr__(self, name, value):
        if name in self.__dict__:
            raise AttributeError('Constants are not changeable!')
        else:
            super().__setattr__(name, value)