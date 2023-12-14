import psycopg2

import sys
import os

current_directory = os.path.dirname(os.path.realpath(__file__))
root_directory = os.path.abspath(os.path.join(current_directory, ".."))
sys.path.append(root_directory)

from utils.database_utils import create_connection


def drop_all_tables():
    try:
        with create_connection() as connection:
            connection.autocommit = True
            with connection.cursor() as cursor:
                # Получаем список всех таблиц в базе данных
                cursor.execute(
                    "SELECT table_name FROM information_schema.tables WHERE table_schema='public';"
                )
                tables = cursor.fetchall()

                # Удаляем каждую таблицу
                for table in tables:
                    cursor.execute(f"DROP TABLE IF EXISTS {table[0]} CASCADE;")

        print("Все таблицы успешно удалены.")
    except psycopg2.Error as e:
        print(f"Ошибка при удалении таблиц: {e}")


def drop_tables():
    try:
        with create_connection() as connection:
            connection.autocommit = True
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    DROP TABLE IF EXISTS services CASCADE
                """
                )

                cursor.execute(
                    """
                    DROP TABLE IF EXISTS service_requests CASCADE
                """
                )

                cursor.execute(
                    """
                    DROP TABLE IF EXISTS users CASCADE
                """
                )

        print("Таблицы успешно удалены.")
    except psycopg2.Error as e:
        print(f"Ошибка при удалении таблиц: {e}")


def create_tables():
    try:
        with create_connection() as connection:
            connection.autocommit = True
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS services (
                        service_id SERIAL PRIMARY KEY,
                        service_name VARCHAR(255) NOT NULL,
                        description TEXT NOT NULL,
                        additional_info TEXT NOT NULL,
                        price INTEGER NOT NULL,
                        image VARCHAR(255) NOT NULL
                    )
                """
                )

                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS users (
                        user_id SERIAL PRIMARY KEY,
                        login VARCHAR(100) NOT NULL,
                        password VARCHAR(255) NOT NULL,
                        role VARCHAR(50) DEFAULT 'user' NOT NULL
                    )
                """
                )

                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS service_requests (
                        service_request_id SERIAL PRIMARY KEY,
                        client_name VARCHAR(255) NOT NULL,
                        car_brand VARCHAR(255) NOT NULL,
                        car_model VARCHAR(255) NOT NULL,
                        service_name VARCHAR(255) NOT NULL,
                        phone_number VARCHAR(20) NOT NULL,
                        user_id INTEGER,
                        FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
                    )
                """
                )

        print("Таблицы успешно созданы.")
    except psycopg2.Error as e:
        print(f"Ошибка при создании таблиц: {e}")
