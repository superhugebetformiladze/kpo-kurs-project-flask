import psycopg2

import sys
import os
current_directory = os.path.dirname(os.path.realpath(__file__))
root_directory = os.path.abspath(os.path.join(current_directory, '..'))
sys.path.append(root_directory)

from utils.database_utils import create_connection


def database_exists(database_name):
    try:
        with create_connection() as connection:
            connection.autocommit = True
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s;", (database_name,))
                exists = cursor.fetchone()

        return exists is not None
    except psycopg2.Error as e:
        print(f"Ошибка при проверке наличия базы данных: {e}")
        return False

def create_database(db_config):
    try:
        if not database_exists(db_config['database']):
            with create_connection() as connection:
                connection.autocommit = True
                with connection.cursor() as cursor:
                    cursor.execute(f"CREATE DATABASE {db_config['database']} ENCODING 'UTF8' TEMPLATE template0")

            print(f"База данных '{db_config['database']}' успешно создана.")
        else:
            print(f"База данных '{db_config['database']}' уже существует.")
    except psycopg2.Error as e:
        print(f"Ошибка при создании базы данных: {e}")
