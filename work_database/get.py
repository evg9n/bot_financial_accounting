import datetime
from datetime import date
from typing import Optional, Union

from loader import environ
from psycopg2 import connect, errors
from logging import getLogger
from traceback import format_exc
from dotenv import load_dotenv
# from os import environ
#
# load_dotenv()


log = getLogger('get_database')

USER = environ.get('USER_NAME')
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


def get_state_date(user_id: int, column_date2: bool = False) -> Optional[datetime.date]:
    """
    Получение текущего даты из состояния
    :param user_id: id пользователя
    :param column_date2: Вторую дату?
    :return: текущая дата из состояния
    """
    sql_query = f"""SELECT {'date2' if column_date2 else 'date'} FROM state WHERE id = {user_id} LIMIT 1"""
    result = get_query(sql_query=sql_query)
    return result[0][0] if result else None


def get_state_max_sheet(user_id) -> Optional[int]:
    """
    Получение текущего max_sheet из состояния
    :param user_id: id пользователя
    :return: текущий max_sheet
    """
    sql_query = f"""SELECT max_sheet FROM state WHERE id = {user_id} LIMIT 1"""
    result = get_query(sql_query=sql_query)
    return result[0][0] if result else None


def get_state_current_sheet(user_id) -> Optional[int]:
    """
    Получение текущего current_sheet из состояния
    :param user_id: id пользователя
    :return: текущий current_sheet
    """
    sql_query = f"""SELECT current_sheet FROM state WHERE id = {user_id} LIMIT 1"""
    result = get_query(sql_query=sql_query)
    return result[0][0] if result else None


def get_for_all_report(user_id: int, name_table: int, date_1: datetime.date, date_2: datetime.date):
    """Получение всех операций с полями sum_operation и type_operation"""
    sql_query = (f"""SELECT sum_operation, type_operation FROM finance_operations 
                    WHERE user_id = {user_id} AND name_table = {name_table} 
                    AND '{date_1}' <= date 
                    AND date <= '{date_2}'""")
    return get_query(sql_query=sql_query)


def get_for_debit_or_credit_report(user_id: int, name_table: int, date_1: datetime.date, date_2: datetime.date,
                                   credit: bool = False):
    """Получение операций расхода или дохода по периоду"""
    sql_query = (f"""SELECT sum_operation, categories_operation FROM finance_operations 
                    WHERE user_id = {user_id} AND name_table = {name_table} 
                    AND type_operation = '{"расход" if credit else "доход"}'
                    AND '{date_1}' <= date 
                    AND date <= '{date_2}'""")
    return get_query(sql_query=sql_query)


def get_all_operations(user_id: int, name_table: int, date_1: datetime.date, date_2: datetime.date,
                       current_sheet: int = 0, count_operation_one_sheet: int = 10, get_all: bool = False):
    """получение всех операций со всеми полями по периоду"""
    if get_all:
        sql_query = (f"""SELECT * FROM finance_operations 
                    WHERE user_id = {user_id} AND name_table = {name_table} AND
                    '{date_1}' <= date AND date <= '{date_2}' ORDER BY date DESC""")
    else:
        sql_query = (f"""SELECT * FROM finance_operations 
                    WHERE user_id = {user_id} AND name_table = {name_table} AND
                    '{date_1}' <= date AND date <= '{date_2}'
                    LIMIT {count_operation_one_sheet} OFFSET {current_sheet * count_operation_one_sheet}""")
    return get_query(sql_query=sql_query)


def get_operation(id_operation: int):
    """Получение конкретной операции по id"""
    sql_query = (f"""SELECT * FROM finance_operations 
                WHERE id = {id_operation} LIMIT 1""")
    result = get_query(sql_query=sql_query)
    return result[0]


def get_users(only_user_id: bool = False) -> list:
    """Получить всех пользователей"""
    if only_user_id:
        sql_query = "SELECT user_id FROM users"
        result = [user_id[0] for user_id in get_query(sql_query=sql_query)]
    else:
        sql_query = "SELECT * FROM users"
        result = get_query(sql_query=sql_query)
    return result


def get_all_finance_operations() -> list:
    """Получить всех финансовых операций"""
    sql_query = "SELECT * FROM finance_operations"
    result = get_query(sql_query=sql_query)
    return result


def get_all_names_finance() -> list:
    """Получить все имена баз"""
    sql_query = "SELECT * FROM names_finance"
    result = get_query(sql_query=sql_query)
    return result


def get_all_state() -> list:
    """Получить всех состояний"""
    sql_query = "SELECT * FROM state"
    result = get_query(sql_query=sql_query)
    return result


def get_old_date(user_id: int, name_table: int) -> date:
    """
    Получить самую старую дату
    :param user_id: id пользователя
    :param name_table: имя финанса
    :return: текущий финанс
    """
    sql_query = (f"""SELECT date FROM finance_operations 
                WHERE user_id = {user_id} AND name_table = {name_table}
                ORDER BY date DESC LIMIT 1""")

    result = get_query(sql_query=sql_query)
    return result[0][0]


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
