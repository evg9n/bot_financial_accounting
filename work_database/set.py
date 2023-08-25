from loader import environ
from telebot.types import Message
from psycopg2 import connect, errors
from logging import getLogger
from traceback import format_exc


log = getLogger('write_database')

USER = environ.get('USER')
NAME_DATABASE = environ.get('NAME_DATABASE')
PASSWORD = environ.get('PASSWORD')
HOST = environ.get('HOST')
PORT = int(environ.get('PORT'))


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
            log.info(f'Добавлен пользователь {user_id} {username}')
            return True
        finally:
            conn.close()
            cursor.close()
    except UnboundLocalError:
        return False


def set_state(user_id: int, state=None) -> bool:
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
            cursor = conn.cursor()
            sql_query = f"""UPDATE state set state = '{"none" if state is None else state}'
                            WHERE ID = {user_id}"""
            cursor.execute(query=sql_query)
            conn.commit()
        except errors.OperationalError:
            log.error(f'Не удалось добавить состояние {state} пользователя {user_id}: {format_exc()}')
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
            log.info(f'Добавлено состояние {state} пользователя {user_id}')
            return True
        finally:
            conn.close()
            cursor.close()
    except UnboundLocalError:
        return False


def set_names_finance(name: str, user_id: int) -> bool:
    """
    записать финанса в names_finance
    :param user_id: id gользователя
    :param name: имя финанса
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
            sql_query = f"""INSERT INTO names_finance (user_id, name_table) 
                            VALUES ({user_id}, '{name}')"""
            cursor.execute(query=sql_query)
            conn.commit()
        except errors.OperationalError:
            log.error(f'Не удалось записать новый финанс {name} для  {user_id}: {format_exc()}')
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
            log.info(f'Записать новый финанс {name} для  {user_id}')
            return True
        finally:
            conn.close()
            cursor.close()
    except UnboundLocalError:
        return False
