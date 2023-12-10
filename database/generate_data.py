from faker import Faker
import random

import psycopg2

fake = Faker()

def generate_service_data(service_id):
    # Предопределенные значения для генерации
    service_names = ["Мойка", "Замена масла", "Шиномонтаж", "Ремонт тормозов", "Диагностика двигателя"]
    additional_infos = [
        "Бесконтактная мойка с применением новейших технологий.",
        "Замена масла с использованием высококачественных масел и фильтров.",
        "Шиномонтаж с балансировкой колес для комфортного вождения.",
        "Качественный ремонт тормозной системы с гарантией безопасности.",
        "Полная диагностика двигателя с использованием современного оборудования."
    ]

    service_name = random.choice(service_names)
    additional_info = random.choice(additional_infos)
    
    description = (
        f"Наш техцентр предлагает услугу {service_name.lower()}. {additional_info}"
    )

    image = f"services/{service_name.lower()}.jpg"
    price = random.randint(500, 3000)

    service_data = {
        'service_id': service_id,
        'service_name': service_name,
        'description': description,
        'additional_info': additional_info,
        'image': image,
        'price': price
    }

    return service_data

def insert_services_data(db_config, num_services):
    try:
        connection = psycopg2.connect(
            host=db_config['host'],
            database=db_config['database'],
            user=db_config['user'],
            password=db_config['password']
        )
        connection.autocommit = True

        cursor = connection.cursor()

        for service_id in range(1, num_services + 1):
            service_data = generate_service_data(service_id)
            cursor.execute('''
                INSERT INTO services (service_id, service_name, description, additional_info, price, image)
                VALUES (%s, %s, %s, %s, %s, %s)
            ''', (
                service_data['service_id'],
                service_data['service_name'],
                service_data['description'],
                service_data['additional_info'],
                service_data['price'],
                service_data['image']
            ))

        cursor.close()
        connection.close()

        print(f"{num_services} данные успешно добавлены в таблицу services.")
    except psycopg2.Error as e:
        print(f"Ошибка при вставке данных в таблицу services: {e}")