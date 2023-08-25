from loader import environ
from telebot.types import Message
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2 import connect, errors
from logging import getLogger
from traceback import format_exc
# from main import bot


log = getLogger('create_database')

USER = environ.get('USER')
NAME_DATABASE = environ.get('NAME_DATABASE')
PASSWORD = environ.get('PASSWORD')
HOST = environ.get('HOST')
PORT = int(environ.get('PORT'))


def create_database() -> bool:
    """
    Создании базы данных
    :return: bool рузультат выполнения
    """
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
    """
    Удаление базы данных
    :return: bool рузультат выполнения
    """
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


def create_table_users() -> bool:
    """
    Созлание таблицы users
    :return: bool рузультат выполнения
    """
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
                            user_id BIGINT UNIQUE NOT NULL,
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


def create_table_names_finance() -> bool:
    """
    Созлание таблицы names_finance
    :return: bool рузультат выполнения
    """
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
            sql_request = f"""CREATE TABLE names_finance (
                            id SERIAL PRIMARY KEY,
                            user_id BIGINT REFERENCES users(user_id) ON DELETE CASCADE NOT NULL,
                            name_table VARCHAR(50) NOT NULL)"""
            cursor.execute(query=sql_request)
            conn.commit()
        except errors.DuplicateTable:
            log.debug(f'Таблица names_finance уже существует: {format_exc()}')
            return True
        except (errors.OperationalError, errors.SyntaxError):
            log.warning(f'Не удалось создать таблицу names_finance: {format_exc()}')
            return False
        else:
            log.info(f'Создана таблица names_finance')
            return True
        finally:
            conn.close()
            cursor.close()
    except UnboundLocalError:
        return False


def create_table_state() -> bool:
    """
    Созлание таблицы names_finance
    :return: bool рузультат выполнения
    """
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
            sql_request = f"""CREATE TABLE state (
                            id BIGINT UNIQUE NOT NULL,
                            user_id BIGINT REFERENCES users(user_id) ON DELETE CASCADE NOT NULL ,
                            state VARCHAR(50) NOT NULL DEFAULT 'none')"""
            cursor.execute(query=sql_request)
            conn.commit()
        except errors.DuplicateTable:
            log.debug(f'Таблица state уже существует: {format_exc()}')
            return True
        except (errors.OperationalError, errors.SyntaxError):
            log.warning(f'Не удалось создать таблицу state: {format_exc()}')
            return False
        else:
            log.info(f'Создана таблица state')
            return True
        finally:
            conn.close()
            cursor.close()
    except UnboundLocalError:
        return False


def create_state_user(user_id: int) -> bool:
    """
    Добавление пользователя в таблицу users
    :param message: объект Message telebot
    :return: bool рузультат выполнения
    """
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
            sql_query = f"""INSERT INTO state (id, user_id, state) 
                            VALUES ({user_id}, {user_id}, 'none')"""
            cursor.execute(query=sql_query)
            conn.commit()
        except errors.OperationalError:
            log.error(f'Не удалось добавить состояние none пользователя {user_id}: {format_exc()}')
            return False
        except errors.UndefinedTable:
            log.error(f'{format_exc()}')
            # create_table_users()
            # cursor.execute(query=sql_query)
            # conn.commit()
            return False
        except errors.DuplicateColumn:
            log.warning(f'{format_exc()}')
            return True
        except errors.UndefinedColumn:
            log.warning(f'{format_exc()}')
            return False
        except errors.UniqueViolation:
            return True
        else:
            log.info(f'Добавлено состояние none пользователя {user_id}')
            return True
        finally:
            conn.close()
            cursor.close()
    except UnboundLocalError:
        return False

