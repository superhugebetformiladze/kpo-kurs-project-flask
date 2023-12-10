import psycopg2


def drop_all_tables(db_config):
    try:
        connection = psycopg2.connect(
            host=db_config['host'],
            database=db_config['database'],
            user=db_config['user'],
            password=db_config['password']
        )
        connection.autocommit = True

        cursor = connection.cursor()

        # Получаем список всех таблиц в базе данных
        cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public';")
        tables = cursor.fetchall()

        # Удаляем каждую таблицу
        for table in tables:
            cursor.execute(f"DROP TABLE IF EXISTS {table[0]} CASCADE;")

        cursor.close()
        connection.close()

        print("Все таблицы успешно удалены.")
    except psycopg2.Error as e:
        print(f"Ошибка при удалении таблиц: {e}")

def drop_tables(db_config):
    try:
        connection = psycopg2.connect(
            host=db_config['host'],
            database=db_config['database'],
            user=db_config['user'],
            password=db_config['password']
        )
        connection.autocommit = True

        cursor = connection.cursor()

        cursor.execute('''
            DROP TABLE IF EXISTS services CASCADE
        ''')

        cursor.execute('''
            DROP TABLE IF EXISTS service_requests CASCADE
        ''')

        cursor.execute('''
            DROP TABLE IF EXISTS users CASCADE
        ''')

        cursor.close()
        connection.close()

        print("Таблицы успешно удалены.")
    except psycopg2.Error as e:
        print(f"Ошибка при удалении таблиц: {e}")

def create_tables(db_config):
    try:
        connection = psycopg2.connect(
            host=db_config['host'],
            database=db_config['database'],
            user=db_config['user'],
            password=db_config['password']
        )
        connection.autocommit = True

        cursor = connection.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS services (
                service_id SERIAL PRIMARY KEY,
                service_name VARCHAR(255) NOT NULL,
                description TEXT NOT NULL,
                additional_info TEXT NOT NULL,
                price INTEGER NOT NULL,
                image VARCHAR(255) NOT NULL
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS service_requests (
                service_request_id SERIAL PRIMARY KEY,
                client_name VARCHAR(255) NOT NULL,
                car_brand VARCHAR(255) NOT NULL,
                car_model VARCHAR(255) NOT NULL,
                service_name VARCHAR(255) NOT NULL,
                phone_number VARCHAR(20) NOT NULL,
                image_path VARCHAR(255) NOT NULL,
                service_id INTEGER REFERENCES services(service_id) ON DELETE CASCADE
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id SERIAL PRIMARY KEY,
                login VARCHAR(100) NOT NULL,
                password VARCHAR(255) NOT NULL
            )
        ''')

        cursor.close()
        connection.close()

        print("Таблицы успешно созданы.")
    except psycopg2.Error as e:
        print(f"Ошибка при создании таблиц: {e}")