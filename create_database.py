from psycopg2 import connect, OperationalError
from os import environ, path
from dotenv import load_dotenv
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


load_dotenv(dotenv_path=path.abspath(path.join('.env')))


def create_database():
    try:
        con = connect(
            user=environ.get('USER'),
            password=environ.get('PASSWORD'),
            host=environ.get('HOST'),
            port=int(environ.get('PORT')),
        )
        con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = con.cursor()
        name_database = environ.get('NAME_DATABASE')
        cursor.execute(f"CREATE DATABASE {name_database}")
        cursor.close()
        conn.close()
    except OperationalError as error:
        print(error)


def create_table_users():
    sql_request = """CREATE TABLE users (
                    user_id BIGINT UNIQUE,
                    username CHARACTER VARYING(50),
                    first_name CHARACTER VARYING(50),
                    last_name CHARACTER VARYING(50),
                    language_code CHARACTER VARYING(5),
                    is_premium boolean,
                    chat_id bigint);"""
    cursor.execute(sql_request)


def write_base_users():
    user_id = 938616711
    username = 'TataYana5'
    first_name = 'Татьяна Корепанова'
    last_name = ''
    language_code = 'ru'
    is_premium = False
    chat_id = 938616711
    insert_query = f"""INSERT INTO users (user_id, username, first_name, last_name, 
                        language_code, is_premium, chat_id) VALUES (
                        {user_id}, '{username}', '{first_name}', '{last_name}',
                        '{language_code}', {is_premium}, {chat_id})"""
    cursor.execute(insert_query)


def drop_database():
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
        cursor.execute(f"DROP DATABASE {name_database}")
    except OperationalError as error:
        print(error)


if __name__ == "__main__":
    # create_database()
    with connect(
            user=environ.get('USER'),
            password=environ.get('PASSWORD'),
            host=environ.get('HOST'),
            port=int(environ.get('PORT')),
            database=environ.get('NAME_DATABASE')
    ) as conn:
        with conn.cursor() as cursor:
            # create_table_users()
            # write_base_users()
            s = cursor.execute('SELECT (user_id) from users')
            print(cursor.rowcount)
            print(cursor.fetchall())
            # insert_query = """INSERT INTO """
