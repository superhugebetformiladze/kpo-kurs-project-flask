from flask_login import current_user
import psycopg2

import sys
import os

current_directory = os.path.dirname(os.path.realpath(__file__))
root_directory = os.path.abspath(os.path.join(current_directory, ".."))
sys.path.append(root_directory)

from utils.database_utils import create_connection


def is_admin():
    return current_user.role == "admin" if current_user.is_authenticated else False


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
                cursor.execute(
                    """
                    DELETE FROM services
                    WHERE service_id = %s
                """,
                    (service_id,),
                )

        print("Услуга успешно удалена.")
    except psycopg2.Error as e:
        print(f"Ошибка при удалении услуги: {e}")

def read_users():
    try:
        with create_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT user_id, login, password, role FROM users
                """
                )
                users = cursor.fetchall()

        return users
    except psycopg2.Error as e:
        print(f"Ошибка при получении списка пользователей: {e}")
        return None

def delete_user(user_id):
    try:
        with create_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    DELETE FROM users
                    WHERE user_id = %s
                """,
                    (user_id,),
                )

        print("Пользователь успешно удален.")
    except psycopg2.Error as e:
        print(f"Ошибка при удалении пользователя: {e}")

def read_requests():
    try:
        with create_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT service_request_id, client_name, car_brand, car_model, service_name, phone_number, user_id FROM service_requests
                """
                )
                requests = cursor.fetchall()

        return requests
    except psycopg2.Error as e:
        print(f"Ошибка при получении списка заявок: {e}")
        return None

def delete_request(request_id):
    try:
        with create_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    DELETE FROM service_requests
                    WHERE service_request_id = %s
                """,
                    (request_id,),
                )

        print("Заявка успешно удалена.")
    except psycopg2.Error as e:
        print(f"Ошибка при удалении заявки: {e}")