import datetime

from loader import environ
from telebot.types import Message
from psycopg2 import connect, errors
from logging import getLogger
from traceback import format_exc


log = getLogger('set_database')

USER = environ.get('USER')
NAME_DATABASE = environ.get('NAME_DATABASE')
PASSWORD = environ.get('PASSWORD')
HOST = environ.get('HOST')
PORT = int(environ.get('PORT'))


def set_query(sql_query: str) -> bool:
    """
    Добавление пользователя в таблицу users
    :param sql_query: sql-запрос
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
            cursor.execute(query=sql_query)
            conn.commit()
        except errors.OperationalError:
            log.error(f'Не удалось выполнить set-запрос {sql_query}: {format_exc()}')
            return False
        except errors.UndefinedTable:
            log.error(f'{format_exc()}')
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
            log.info(f'Выполнен set-запрос {sql_query}')
            return True
        finally:
            conn.close()
            cursor.close()
    except UnboundLocalError:
        return False


def set_users(message: Message) -> bool:
    """
    Добавление пользователя в таблицу users
    :param message: объект Message telebot
    :return: bool рузультат выполнения
    """
    from_user = message.from_user
    user_id = from_user.id
    username = from_user.username
    first_name = from_user.first_name
    last_name = from_user.last_name
    language_code = from_user.language_code
    chat_id = message.chat.id
    sql_query = f"""INSERT INTO users (user_id, username, first_name, last_name, 
                    language_code, chat_id) 
                    VALUES ({user_id}, '{username}', '{first_name}', '{last_name}', 
                    '{language_code}', {chat_id})"""
    return set_query(sql_query=sql_query)


def set_state(user_id: int, state=None) -> bool:
    """
    Изменение в таблице состояние само состояние
    :param user_id: id пользователя
    :return: bool результат выполнения
    """
    sql_query = f"""UPDATE state set state = '{"none" if state is None else state}'
                    WHERE ID = {user_id}"""
    return set_query(sql_query=sql_query)


def set_state_name_table(user_id: int, name_table: str) -> bool:
    """
        Изменение в таблице состояние текущий финанс
        :param user_id: id пользователя
        :param name_table: наиминование финанса
        :return: bool результат выполнения
        """
    sql_query = f"""UPDATE state set name_table = '{name_table}'
                        WHERE ID = {user_id}"""
    return set_query(sql_query=sql_query)


def set_state_sum_operation(user_id: int, sum_operation: float = None) -> bool:
    """
        Изменение в таблице состояние суммы операции
        :param user_id: id пользователя
        :param sum_operation: сохранение суммы
        :return: bool результат выполнения
        """
    sql_query = f"""UPDATE state set sum_operation = {sum_operation}
                        WHERE ID = {user_id}"""
    return set_query(sql_query=sql_query)


def set_state_message_id(user_id: int, message_id: int = None) -> bool:
    """
        Изменение в таблице состояние message_id
        :param user_id: id пользователя
        :param message_id: message_id
        :return: bool результат выполнения
        """
    sql_query = f"""UPDATE state set message_id = {message_id}
                        WHERE ID = {user_id}"""
    return set_query(sql_query=sql_query)


def set_state_date(user_id: int, date: datetime.date = None, column_date2: bool = False) -> bool:
    """
        Изменение в таблице состояние date
        :param user_id: id пользователя
        :param date: YYYY-MM_DD
        :return: bool результат выполнения
        """
    column = 'date2' if column_date2 else 'date'
    sql_query = f"""UPDATE state set {column} = '{date}'
                        WHERE ID = {user_id}"""
    return set_query(sql_query=sql_query)


def set_state_categories_operation(user_id: int, categorie_operation: int = None) -> bool:
    """
    Изменение в таблице состояние set_state_categories_operation
    :param user_id: id пользователя
    :param categorie_operation: categorie_operation
    :return: bool результат выполнения
    """
    sql_query = f"""UPDATE state set categories_operation = '{categorie_operation}'
                    WHERE ID = {user_id}"""
    return set_query(sql_query=sql_query)


def set_state_finance_operations_id(user_id: int, finance_operations_id: int = None) -> bool:
    """
        Изменение в таблице состояние id текущей операции
        :param user_id: id пользователя
        :param finance_operations_id: id текущей операции
        :return: bool результат выполнения
        """
    sql_query = f"""UPDATE state set finance_operations_id = '{finance_operations_id}'
                        WHERE ID = {user_id}"""
    return set_query(sql_query=sql_query)


def set_names_finance(name: str, user_id: int, delete: bool = False) -> bool:
    """
    записать финанса в names_finance
    :param user_id: id gользователя
    :param name: имя финанса
    :parm delete: Удалить?
    :return: bool рузультат выполнения
    """
    if delete:
        sql_query = f"DELETE FROM names_finance WHERE user_id = {user_id} AND name_table = '{name}'"
    else:
        sql_query = f"""INSERT INTO names_finance (user_id, name_table) 
                        VALUES ({user_id}, '{name}')"""
    return set_query(sql_query=sql_query)


def set_state_user(user_id: int) -> bool:
    """
    Добавление пользователя в таблицу state
    :param user_id: id пользователя
    :return: bool результат выполнения
    """
    sql_query = f"""INSERT INTO state (id, user_id, state)
                    VALUES ({user_id}, {user_id}, 'none')"""
    return set_query(sql_query=sql_query)
