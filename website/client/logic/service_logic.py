import psycopg2

import sys
import os
current_directory = os.path.dirname(os.path.realpath(__file__))
root_directory = os.path.abspath(os.path.join(current_directory, '..'))
sys.path.append(root_directory)

from utils.database_utils import create_connection

def read_services():
    try:
        with create_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute('''
                    SELECT service_id, service_name, description, additional_info, price, image FROM services
                ''')
                services = cursor.fetchall()

        return services
    except psycopg2.Error as e:
        print(f"Ошибка при получении списка услуг: {e}")
        return None

def read_service_by_id(service_id):
    try:
        with create_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute('''
                    SELECT service_name, description, additional_info, price, image
                    FROM services
                    WHERE service_id = %s
                ''', (service_id,))
                service = cursor.fetchone()

        return service
    except psycopg2.Error as e:
        print(f"Ошибка при получении данных об услуге: {e}")
        return None
    
def read_all_services_except(excluded_service_id):
    try:
        with create_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute('''
                    SELECT service_id, service_name, description, additional_info, price, image
                    FROM services
                    WHERE service_id != %s
                ''', (excluded_service_id,))
                services = cursor.fetchall()

        return services
    except psycopg2.Error as e:
        print(f"Ошибка при получении списка услуг: {e}")
        return None
