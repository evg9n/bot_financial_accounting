from loader import environ
from telebot.types import Message
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2 import connect, errors
from logging import getLogger
from traceback import format_exc
# from main import bot


log = getLogger('work_database')

USER = environ.get('USER')
NAME_DATABASE = environ.get('NAME_DATABASE')
PASSWORD = environ.get('PASSWORD')
HOST = environ.get('HOST')
PORT = int(environ.get('PORT'))


def create_database() -> bool:
    try:
        try:
            conn = connect(
                user=environ.get('USER'),
                password=environ.get('PASSWORD'),
                host=environ.get('HOST'),
                port=int(environ.get('PORT')),
            )
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cursor = conn.cursor()
            name_database = environ.get('NAME_DATABASE')
            cursor.execute(query=f"CREATE DATABASE {name_database}")
            cursor.close()
            conn.close()
        except errors.DuplicateDatabase:
            log.debug(f'База данных {NAME_DATABASE} уже существует: {format_exc()}')
            return True
        except errors.OperationalError:
            log.warning(f'Не удалось создать создать базу данных {NAME_DATABASE}: {format_exc()}')
            return False
        else:
            log.info(f'Создана база данных {NAME_DATABASE}')
            return True
        finally:
            conn.close()
            cursor.close()
    except UnboundLocalError:
        pass


def drop_database() -> bool:
    try:
        try:
            conn = connect(
                user=environ.get('USER'),
                password=environ.get('PASSWORD'),
                host=environ.get('HOST'),
                port=int(environ.get('PORT')),
            )
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cursor = conn.cursor()
            name_database = environ.get('NAME_DATABASE')
            cursor.execute(query=f"DROP DATABASE {name_database}")
            cursor.close()
            conn.close()
        except errors.ObjectInUse:
            log.warning(f'{format_exc()}')
        except errors.InvalidCatalogName:
            log.debug(f'База данных {NAME_DATABASE} не существует: {format_exc()}')
            return False
        else:
            log.info(f'Удалена база данных {NAME_DATABASE}')
            return True
        finally:
            conn.close()
            cursor.close()
    except UnboundLocalError:
        return False


def create_table_users():
    try:
        try:
            conn = connect(
                    user=USER,
                    password=PASSWORD,
                    database=NAME_DATABASE,
                    host=HOST,
                    port=PORT
            )
            cursor = conn.cursor()
            sql_request = f"""CREATE TABLE users (
                            user_id BIGINT UNIQUE,
                            username CHARACTER VARYING(50),
                            first_name CHARACTER VARYING(50),
                            last_name CHARACTER VARYING(50),
                            language_code CHARACTER VARYING(10),
                            chat_id bigint)"""
            cursor.execute(query=sql_request)
            conn.commit()
        except errors.DuplicateTable:
            log.debug(f'Таблица users уже существует: {format_exc()}')
            return True
        except errors.OperationalError:
            log.warning(f'Не удалось создать таблицу users: {format_exc()}')
            return False
        else:
            log.info(f'Создана таблица users')
            return True
        finally:
            conn.close()
            cursor.close()
    except UnboundLocalError:
        return False


def add_users(message: Message):
    """
    Добавление пользователя в таблицу users
    """
    from_user = message.from_user
    user_id = from_user.id
    username = from_user.username
    first_name = from_user.first_name
    last_name = from_user.last_name
    language_code = from_user.language_code
    chat_id = message.chat.id
    try:
        try:
            conn = connect(
                user=USER,
                password=PASSWORD,
                database=NAME_DATABASE,
                host=HOST,
                port=PORT
            )
            cursor =  conn.cursor()
            sql_query = f"""INSERT INTO users (user_id, username, first_name, last_name, 
                            language_code, chat_id) 
                            VALUES ({user_id}, '{username}', '{first_name}', '{last_name}', 
                            '{language_code}', {chat_id})"""
            cursor.execute(query=sql_query)
            conn.commit()
        except errors.OperationalError:
            log.error(f'Не удалось добавить пользователя {user_id} {username}: {format_exc()}')
            return False
        except errors.UndefinedTable:
            log.error(f'{format_exc()}')
            create_table_users()
            cursor.execute(query=sql_query)
            conn.commit()
        except errors.DuplicateColumn:
            log.warning(f'{format_exc()}')
        except errors.UndefinedColumn:
            log.warning(f'{format_exc()}')
        except errors.UniqueViolation:
            return True
        else:
            log.info(f'Добавлен пользователь {user_id} {username}')
            return True
        finally:
            conn.close()
            cursor.close()
    except UnboundLocalError:
        return False


if __name__ == "__main__":
    # create_database()
    # create_table_users()
    drop_database()
