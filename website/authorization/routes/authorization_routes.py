from flask import Blueprint, flash, redirect, render_template, request, url_for

import sys
import os

from flask_login import LoginManager, current_user, login_required, login_user, logout_user

current_directory = os.path.dirname(os.path.realpath(__file__))
root_directory = os.path.abspath(os.path.join(current_directory, ".."))
sys.path.append(root_directory)

from logic.authorization_logic import (
    User,
    check_password,
    create_user,
    get_hashed_password,
    hash_password,
    is_login_exists,
    load_user_info_from_database,
    load_user_info_from_database_with_id,
)

auth_bp = Blueprint("auth", __name__)

login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    user_info = load_user_info_from_database_with_id(user_id)
    if user_info:
        return User(user_id, user_info["login"], user_info["role"])
    else:
        return None


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        login = request.form["login"]
        password = request.form["password"]

        if is_login_exists(login):
            error_message = "Пользователь с таким логином уже существует."
            flash(error_message, "error")
            return redirect("register")

        hashed_password = hash_password(password)

        if create_user(login, hashed_password):
            return redirect("login")
        else:
            error_message = "Произошла ошибка. Пожалуйста, попробуйте снова."
            flash(error_message, "error")
            return redirect("register")

    else:
        return render_template("auth/register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        login = request.form["login"]
        password = request.form["password"]

        hashed_password = get_hashed_password(login)

        user_info = load_user_info_from_database(login)

        if hashed_password and check_password(hashed_password, password):
            user = User(user_info["user_id"], login, user_info["role"])
            login_user(user)
            print("Успешный вход")
            user_info = {"login": current_user.get_id(), "role": current_user.role}
            return redirect(url_for("client.index"))
        else:
            error_message = "Неверные учетные данные. Пожалуйста, проверьте логин и пароль."
            flash(error_message, "error")
            return render_template("auth/login.html")
    else:
        return render_template("auth/login.html")


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    print("Успешный выход")
    return redirect(url_for("client.index"))
