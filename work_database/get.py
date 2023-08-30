from typing import Optional, Union

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


def get_query(sql_query: str) -> list:
    """
    SQL-запрос
    :param sql_query: sql-запрос
    :return: список или кортеж с результатом
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
            cursor = conn.cursor()
            cursor.execute(query=sql_query)
            result = cursor.fetchall()
        except errors.OperationalError:
            log.error(f'Не удалось выполнить запрос {sql_query}: {format_exc()}')
            return result
        except errors.UndefinedTable:
            log.error(f'{format_exc()}')
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
            log.info(f'Выполнен запрос {sql_query}')
            return result
        finally:
            conn.close()
            cursor.close()
    except UnboundLocalError:
        return result


def get_names_finance(user_id) -> list:
    """
    Получение списка финансов пользователя
    :param user_id: id пользователя
    :return: список с результатом
    """
    sql_query = f"""SELECT name_table FROM names_finance WHERE user_id = {user_id}"""
    result = get_query(sql_query=sql_query)
    return [element[0] for element in result]


def get_names_finance_id(user_id: int, name: str) -> int:
    """
    Получение id финансf
    :param user_id: id пользователя
    :return: ID финанса
    """
    sql_query = f"""SELECT id FROM names_finance WHERE user_id = {user_id} AND name_table = '{name}' LIMIT 1"""
    result = get_query(sql_query=sql_query)
    return result[0][0]


def get_state(user_id, get_all: bool = False) -> Union[str, tuple]:
    """
    Получение состояние пользователя
    :param user_id: id пользователя
    :return: состояние пользователя
    """
    if get_all:
        sql_query = f"""SELECT * FROM state WHERE id = {user_id} LIMIT 1"""
        result = get_query(sql_query=sql_query)
        return result[0] if result else 'none'
    else:
        sql_query = f"""SELECT state FROM state WHERE id = {user_id} LIMIT 1"""
        result = get_query(sql_query=sql_query)
        return result[0][0] if result else 'none'


def get_state_name_table(user_id) -> Optional[str]:
    """
    Получение текущего финанса из состояния
    :param user_id: id пользователя
    :return: текущий финанс
    """
    sql_query = f"""SELECT name_table FROM state WHERE id = {user_id} LIMIT 1"""
    result = get_query(sql_query=sql_query)
    return result[0][0] if result else None


def get_state_message_id(user_id) -> Optional[int]:
    """
    Получение текущего message_id из состояния
    :param user_id: id пользователя
    :return: текущий финанс
    """
    sql_query = f"""SELECT message_id FROM state WHERE id = {user_id} LIMIT 1"""
    result = get_query(sql_query=sql_query)
    return result[0][0] if result else None


def get_state_sum_operation(user_id) -> Optional[float]:
    """
    Получение текущего sum_operation из состояния
    :param user_id: id пользователя
    :return: текущий sum_operation
    """
    sql_query = f"""SELECT sum_operation FROM state WHERE id = {user_id} LIMIT 1"""
    result = get_query(sql_query=sql_query)
    return result[0][0] if result else None


def get_state_type_operation(user_id) -> Optional[str]:
    """
    Получение текущего sum_operation из состояния
    :param user_id: id пользователя
    :return: текущий sum_operation
    """
    sql_query = f"""SELECT type_operation FROM state WHERE id = {user_id} LIMIT 1"""
    result = get_query(sql_query=sql_query)
    return result[0][0] if result else None


def get_all_report(user_id: int, name_table: int):
    sql_query = (f'SELECT sum_operation, type_operation FROM finance_operations '
                 f'WHERE user_id = {user_id} AND name_table = {name_table}')
    return get_query(sql_query=sql_query)


def get_test():
    """
    Получение текущего финанса из состояния
    :param user_id: id пользователя
    :return: текущий финанс
    """
    sql_query = f"""SELECT * FROM state"""
    result = get_query(sql_query=sql_query)
    # print(result[0][4] + 15)
    # return result[0][0] if result else 'none'
