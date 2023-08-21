from psycopg2 import connect, OperationalError
from os import environ, path
from dotenv import load_dotenv
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

p = path.abspath(path.join('.env'))
print(p)
load_dotenv(dotenv_path=p)


def create_database():
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
        cursor.execute(f"CREATE DATABASE {name_database}")
        cursor.close()
        conn.close()
    except OperationalError as error:
        print(error)


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
    drop_database()

