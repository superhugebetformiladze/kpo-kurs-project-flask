import psycopg2

import sys
import os

current_directory = os.path.dirname(os.path.realpath(__file__))
root_directory = os.path.abspath(os.path.join(current_directory, ".."))
sys.path.append(root_directory)

from utils.database_utils import create_connection


def save_request(request_data):
    try:
        with create_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO service_requests (client_name, car_brand, car_model, service_name, phone_number, user_id)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                    (
                        request_data["client_name"],
                        request_data["car_brand"],
                        request_data["car_model"],
                        request_data["service_name"],
                        request_data["phone_number"],
                        request_data["user_id"],
                    ),
                )
    except psycopg2.Error as e:
        print(f"Ошибка при сохранении заявки в базе данных: {e}")


def read_requests_by_user_id(user_id):
    try:
        with create_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT client_name, car_brand, car_model, service_name, phone_number
                    FROM service_requests
                    WHERE user_id = %s
                """,
                    (user_id,),
                )
                service_request = cursor.fetchall()

        return service_request
    except psycopg2.Error as e:
        print(f"Ошибка при получении данных о заявке: {e}")
        return None
