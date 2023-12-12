import psycopg2

import sys
import os

current_directory = os.path.dirname(os.path.realpath(__file__))
root_directory = os.path.abspath(os.path.join(current_directory, ".."))
sys.path.append(root_directory)

from utils.database_utils import create_connection


def create_service(service_data):
    try:
        with create_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                            INSERT INTO services (service_name, description, additional_info, price, image)
                            VALUES (%s, %s, %s, %s, %s)
                        """,
                    (
                        service_data["service_name"],
                        service_data["description"],
                        service_data["additional_info"],
                        service_data["price"],
                        service_data["image"],
                    ),
                )

        print("Услуга успешно добавлена.")
        return True
    except psycopg2.Error as e:
        print(f"Ошибка при добавлении услуги: {e}")
        return False


def update_service(service_id, new_service_data):
    try:
        with create_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE services
                    SET service_name = %s,
                        description = %s,
                        additional_info = %s,
                        price = %s,
                        image = %s
                    WHERE service_id = %s
                """,
                    (
                        new_service_data["service_name"],
                        new_service_data["description"],
                        new_service_data["additional_info"],
                        new_service_data["price"],
                        new_service_data["image"],
                        service_id,
                    ),
                )
                
        print("Услуга успешно обновлена.")
    except psycopg2.Error as e:
        print(f"Ошибка при обновлении услуги: {e}")


def delete_service(service_id):
    try:
        with create_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute('''
                    DELETE FROM services
                    WHERE service_id = %s
                ''', (service_id,))
                
        print("Услуга успешно удалена.")
    except psycopg2.Error as e:
        print(f"Ошибка при удалении услуги: {e}")