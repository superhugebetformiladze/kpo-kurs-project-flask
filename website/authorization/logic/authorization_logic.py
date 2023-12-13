from flask_login import UserMixin
import psycopg2
import bcrypt

import sys
import os

current_directory = os.path.dirname(os.path.realpath(__file__))
root_directory = os.path.abspath(os.path.join(current_directory, ".."))
sys.path.append(root_directory)

from utils.database_utils import create_connection
from enums.roles import Role


class User(UserMixin):
    def __init__(self, user_id, login, role):
        self.id = user_id
        self.login = login
        self.role = role


def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed_password.decode("utf-8")


def check_password(hashed_password, user_password):
    return bcrypt.checkpw(
        user_password.encode("utf-8"), hashed_password.encode("utf-8")
    )


def create_user(login, password, role=Role.USER.value):
    try:
        if is_login_exists(login):
            print(f"Пользователь с логином {login} уже существует.")
            return False

        with create_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO users (login, password, role)
                    VALUES (%s, %s, %s)
                    """,
                    (login, password, role),
                )

        print(f"Пользователь {role} успешно создан.")
        return True
    except psycopg2.Error as e:
        print(f"Ошибка при создании пользователя {role}: {e}")
        return False


def is_login_exists(login):
    try:
        with create_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT EXISTS(SELECT 1 FROM users WHERE login = %s)
                    """,
                    (login,),
                )
                return cursor.fetchone()[0]
    except psycopg2.Error as e:
        print(f"Ошибка при проверке существования логина: {e}")
        return False


def get_hashed_password(login):
    try:
        with create_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT password FROM users
                    WHERE login = %s
                """,
                    (login,),
                )
                password = cursor.fetchone()

        return password[0] if password else None
    except psycopg2.Error as e:
        print(f"Ошибка при получении пароля пользователя: {e}")
        return None


def load_user_info_from_database(login):
    try:
        with create_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT user_id, role FROM users
                    WHERE login = %s
                    """,
                    (login,),
                )
                user_info = cursor.fetchone()

        if user_info:
            user_id, role = user_info
            return {"user_id": user_id, "role": role}
        else:
            return None
    except psycopg2.Error as e:
        print(f"Ошибка при загрузке информации о пользователе из базы данных: {e}")
        return None


def load_user_info_from_database_with_id(user_id):
    try:
        with create_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT login, role FROM users
                    WHERE user_id = %s
                    """,
                    (user_id,),
                )
                user_info = cursor.fetchone()

        if user_info:
            login, role = user_info
            return {"login": login, "role": role}
        else:
            return None
    except psycopg2.Error as e:
        print(f"Ошибка при загрузке информации о пользователе из базы данных: {e}")
        return None
