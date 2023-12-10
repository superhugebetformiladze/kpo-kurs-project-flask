from faker import Faker
import random

import psycopg2

fake = Faker()

def generate_service_data(service_id):
    service_name = fake.word()
    description = (
        f"Наш техцентр предлагает услугу {service_name.lower()}. Это процедура, "
        f"которая позволяет вернуть кузову идеальную форму после даже серьезного повреждения. "
        f"В результате {service_name.lower()} ваш автомобиль будет выглядеть как новый.\n\n"
        f"Мы используем только профессиональное оборудование и качественные материалы, "
        f"чтобы обеспечить наилучший результат. Наши специалисты проходят регулярное обучение и "
        f"имеют большой опыт работы.\n\n"
        f"Наши услуги доступны по приемлемым ценам и мы применяем индивидуальный подход к каждому "
        f"клиенту. Вы можете быть уверены в качестве нашей работы и мы гарантируем быстрое выполнение "
        f"заказа.\n\n"
        f"Если у вас есть проблемы, связанные с {service_name.lower()}, свяжитесь с нашим техцентром и "
        f"мы поможем вернуть ваш автомобиль в идеальное состояние. Вы можете быть уверены в качестве и "
        f"профессионализме нашей работы."
    )
    additional_info = fake.paragraph(nb_sentences=random.randint(1, 3))
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