from flask_login import UserMixin
import psycopg2
import bcrypt

import sys
import os

current_directory = os.path.dirname(os.path.realpath(__file__))
root_directory = os.path.abspath(os.path.join(current_directory, ".."))
sys.path.append(root_directory)

from utils.database_utils import create_connection


class User(UserMixin):
    def __init__(self, user_id, is_admin=False):
        self.id = user_id
        self.is_admin = is_admin
        
def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed_password.decode("utf-8")


def check_password(hashed_password, user_password):
    return bcrypt.checkpw(
        user_password.encode("utf-8"), hashed_password.encode("utf-8")
    )


def create_user(login, password, is_admin=False):
    try:
        with create_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO users (login, password, is_admin)
                    VALUES (%s, %s, %s)
                """,
                    (login, password, is_admin),
                )

        print("Пользователь успешно создан.")
        return True
    except psycopg2.Error as e:
        print(f"Ошибка при создании пользователя: {e}")
        return False

def get_hashed_password(login):
    try:
        with create_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute('''
                    SELECT password FROM users
                    WHERE login = %s
                ''', (login,))
                password = cursor.fetchone()

        return password[0] if password else None
    except psycopg2.Error as e:
        print(f"Ошибка при получении пароля пользователя: {e}")
        return None     