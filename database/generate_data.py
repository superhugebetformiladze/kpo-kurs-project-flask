from faker import Faker
import random

import psycopg2

import sys
import os
current_directory = os.path.dirname(os.path.realpath(__file__))
root_directory = os.path.abspath(os.path.join(current_directory, '..'))
sys.path.append(root_directory)

from utils.database_utils import create_connection
from website.authorization.logic.authorization_logic import create_user, hash_password

fake = Faker()

def generate_service_data():
    # Предопределенные значения для генерации
    service_names = ["Мойка", "Замена масла", "Шиномонтаж", "Ремонт тормозов", "Диагностика двигателя"]
    image_names = ["diagnostika-avtomobilya", "Kompyuternaya-diagnostika", "kuzovnoy-remont", "shod-razval", "zamena-masla"]
    additional_infos = [
        "Бесконтактная мойка с применением новейших технологий.",
        "Замена масла с использованием высококачественных масел и фильтров.",
        "Шиномонтаж с балансировкой колес для комфортного вождения.",
        "Качественный ремонт тормозной системы с гарантией безопасности.",
        "Полная диагностика двигателя с использованием современного оборудования."
    ]

    service_name = random.choice(service_names)
    image_name = random.choice(image_names)
    additional_info = random.choice(additional_infos)
    
    description = (
        f"Наш техцентр предлагает услугу {service_name.lower()}. {additional_info}"
    )

    image = f"\static/images/client/services/{image_name.lower()}.jpg"
    price = random.randint(500, 3000)

    service_data = {
        'service_name': service_name,
        'description': description,
        'additional_info': additional_info,
        'image': image,
        'price': price
    }

    return service_data

def insert_services_data(num_services):
    try:
        with create_connection() as connection:
            with connection.cursor() as cursor:
                for services in range(1, num_services + 1):
                    service_data = generate_service_data()
                    cursor.execute('''
                        INSERT INTO services (service_name, description, additional_info, price, image)
                        VALUES (%s, %s, %s, %s, %s)
                    ''', (
                        service_data['service_name'],
                        service_data['description'],
                        service_data['additional_info'],
                        service_data['price'],
                        service_data['image']
                    ))

        print(f"{num_services} данные успешно добавлены в таблицу services.")
    except psycopg2.Error as e:
        print(f"Ошибка при вставке данных в таблицу services: {e}")

def generate_admin_data():
    admin_data = {
        'login': 'admin',
        'password': 'admin1234',
        'is_admin': True
    }

    hashed_password = hash_password(admin_data['password'])

    create_user(admin_data['login'], hashed_password, admin_data['is_admin'])

def insert_admin_data():
    try:
        with create_connection() as connection:
            with connection.cursor() as cursor:
                admin_data = generate_admin_data()
                cursor.execute('''
                    INSERT INTO users (login, password, is_admin)
                    VALUES (%s, %s, %s)
                ''', (
                    admin_data['login'],
                    admin_data['password'],
                    admin_data['is_admin']
                ))

        print("Администратор успешно создан")
    except psycopg2.Error as e:
        print(f"Ошибка при вставке данных в таблицу users: {e}")
