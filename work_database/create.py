from loader import environ
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2 import connect, errors
from logging import getLogger
from traceback import format_exc


log = getLogger('create_database')

USER = environ.get('USER_NAME')
NAME_DATABASE = environ.get('NAME_DATABASE')
PASSWORD = environ.get('PASSWORD')
HOST = environ.get('HOST')
PORT = int(environ.get('PORT'))


def connect_database(with_database: bool = False) -> connect:
    """
    Подключение к postgresql
    :param with_database: Подключиться к БД
    """
    if with_database:
        return connect(
            user=USER,
            password=PASSWORD,
            database=NAME_DATABASE,
            host=HOST,
            port=PORT
        )
    else:
        return connect(
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT
        )


def create_query(sql_query: str, with_database=False) -> bool:
    try:
        try:

            if with_database:
                conn = connect_database(with_database=with_database)
            else:
                conn = connect_database()
                conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

            cursor = conn.cursor()
            cursor.execute(query=sql_query)
        except (errors.DuplicateDatabase, errors.DuplicateTable):
            log.debug(f'Запрос {sql_query} не выполнен по причине дубликата: {format_exc()}')
            return True
        except errors.OperationalError:
            log.warning(f'Запрос {sql_query} не ужалось выполнить: {format_exc()}')
            return False
        else:
            log.info(f'Выполнен запрос {sql_query}')
            conn.commit()
            return True
        finally:
            conn.close()
            cursor.close()
    except UnboundLocalError:
        return False


def create_database() -> bool:
    """
    Создании базы данных
    :return: bool рузультат выполнения
    """
    name_database = environ.get('NAME_DATABASE')
    sql_query = f"CREATE DATABASE {name_database}"
    return create_query(sql_query=sql_query)


def drop_database() -> bool:
    """
    Удаление базы данных
    :return: bool рузультат выполнения
    """
    name_database = environ.get('NAME_DATABASE')
    sql_query = f"DROP DATABASE {name_database}"
    return create_query(sql_query=sql_query)


def create_table_users() -> bool:
    """
    Созлание таблицы users
    :return: bool рузультат выполнения
    """

    sql_query = f"""CREATE TABLE users (
                                user_id BIGINT UNIQUE NOT NULL,
                                username CHARACTER VARYING(50),
                                first_name CHARACTER VARYING(50),
                                last_name CHARACTER VARYING(50),
                                language_code CHARACTER VARYING(10),
                                chat_id bigint)"""
    return create_query(sql_query=sql_query, with_database=True)


def create_table_names_finance() -> bool:
    """
    Созлание таблицы names_finance
    :return: bool рузультат выполнения
    """
    sql_query = f"""CREATE TABLE names_finance (
                                id BIGSERIAL PRIMARY KEY,
                                user_id BIGINT REFERENCES users(user_id) ON DELETE CASCADE NOT NULL,
                                name_table VARCHAR(50) NOT NULL)"""
    return create_query(sql_query=sql_query, with_database=True)


def create_table_state() -> bool:
    """
    Созлание таблицы state
    :return: bool рузультат выполнения
    """
    sql_query = f"""CREATE TABLE state (
                                id BIGINT UNIQUE NOT NULL,
                                user_id BIGINT REFERENCES users(user_id) ON DELETE CASCADE NOT NULL ,
                                state VARCHAR(50) NOT NULL DEFAULT 'none',
                                name_table VARCHAR(50) DEFAULT NULL,
                                sum_operation NUMERIC(21, 2) DEFAULT 0.00,
                                type_operation VARCHAR(6),
                                finance_operations_id BIGINT DEFAULT NULL, 
                                categories_operation VARCHAR(50),
                                message_id BIGINT, 
                                date DATE,
                                date2 DATE,
                                max_sheet BIGINT,
                                current_sheet BIGINT
                                )"""
    return create_query(sql_query=sql_query, with_database=True)


def create_table_finance_operations() -> bool:
    """
    Созлание таблицы finance_operations
    :return: bool рузультат выполнения
    """
    sql_query = f"""CREATE TABLE finance_operations (
                                id BIGSERIAL PRIMARY KEY,
                                user_id BIGINT REFERENCES users(user_id) ON DELETE CASCADE NOT NULL,
                                name_table BIGINT REFERENCES names_finance(id) ON DELETE CASCADE NOT NULL,
                                sum_operation NUMERIC(21, 2) NOT NULL,
                                type_operation VARCHAR(6),
                                categories_operation VARCHAR(50),
                                name_operation VARCHAR(500),
                                date DATE NOT NULL)"""
    return create_query(sql_query=sql_query, with_database=True)


# def create_state_user(user_id: int) -> bool:
#     """
#     Добавление пользователя в таблицу state
#     :param user_id: id пользователя
#     :return: bool результат выполнения
#     """
#     sql_query = f"""INSERT INTO state (id, user_id, state)
#                     VALUES ({user_id}, {user_id}, 'none')"""
#     return create_query(sql_query=sql_query, with_database=True)
