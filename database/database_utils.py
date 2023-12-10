import psycopg2

def database_exists(db_config, database_name):
    try:
        connection = psycopg2.connect(
            host=db_config['host'],
            user=db_config['user'],
            password=db_config['password']
        )
        connection.autocommit = True
        cursor = connection.cursor()

        cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s;", (database_name,))
        exists = cursor.fetchone()

        cursor.close()
        connection.close()

        return exists is not None
    except psycopg2.Error as e:
        print(f"Ошибка при проверке наличия базы данных: {e}")
        return False

def create_database(db_config):
    try:
        if not database_exists(db_config, db_config['database']):
            connection = psycopg2.connect(
                host=db_config['host'],
                user=db_config['user'],
                password=db_config['password']
            )
            connection.autocommit = True
            cursor = connection.cursor()

            cursor.execute(f"CREATE DATABASE {db_config['database']} ENCODING 'UTF8' TEMPLATE template0")

            cursor.close()
            connection.close()

            print(f"База данных '{db_config['database']}' успешно создана.")
        else:
            print(f"База данных '{db_config['database']}' уже существует.")
    except psycopg2.Error as e:
        print(f"Ошибка при создании базы данных: {e}")
