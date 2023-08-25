from loader import environ
from telebot.types import Message
from psycopg2 import connect, errors
from logging import getLogger
from traceback import format_exc


log = getLogger('get_database')

USER = environ.get('USER')
NAME_DATABASE = environ.get('NAME_DATABASE')
PASSWORD = environ.get('PASSWORD')
HOST = environ.get('HOST')
PORT = int(environ.get('PORT'))


def get_names_finance(user_id) -> list:
    """
    Получение списка финансов пользователя
    :param user_id: id пользователя
    :return: список с результатом
    """
    result = list()
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
            sql_query = f"""SELECT name_table FROM names_finance WHERE user_id = {user_id}"""
            cursor.execute(query=sql_query)
            result = cursor.fetchall()
        except errors.OperationalError:
            log.error(f'Не удалось найти пользователя {user_id} : {format_exc()}')
            return result
        except errors.UndefinedTable:
            log.error(f'{format_exc()}')
            # create_table_users()
            # cursor.execute(query=sql_query)
            # conn.commit()
            return result
        except errors.DuplicateColumn:
            log.warning(f'{format_exc()}')
            return result
        except errors.UndefinedColumn:
            log.warning(f'{format_exc()}')
            return result
        except errors.UniqueViolation:
            return result
        else:
            log.info(f'Получены финансы пользователя {user_id}')
            return result
        finally:
            conn.close()
            cursor.close()
    except UnboundLocalError:
        return result


def get_state(user_id):
    """
    Получение состояние пользователя
    :param user_id: id пользователя
    :return: состояние пользователя
    """
    result = 'none'
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
            sql_query = f"""SELECT state FROM state WHERE id = {user_id} LIMIT 1"""
            cursor.execute(query=sql_query)
            # print(1111111111111111111111111, cursor.fetchone()[0])
            result = cursor.fetchone()[0]
        except errors.OperationalError:
            log.error(f'Не удалось найти пользователя {user_id} : {format_exc()}')
            return result
        except errors.UndefinedTable:
            log.error(f'{format_exc()}')
            # create_table_users()
            # cursor.execute(query=sql_query)
            # conn.commit()
            return result
        except errors.DuplicateColumn:
            log.warning(f'{format_exc()}')
            return result
        except errors.UndefinedColumn:
            log.warning(f'{format_exc()}')
            return result
        except errors.UniqueViolation:
            return result
        else:
            log.info(f'Получены состояние пользователя {user_id}')
            return result
        finally:
            conn.close()
            cursor.close()
    except UnboundLocalError:
        return result
