from flask import Blueprint, redirect, render_template, request, url_for

import sys
import os

from flask_login import LoginManager, current_user, login_user, logout_user

current_directory = os.path.dirname(os.path.realpath(__file__))
root_directory = os.path.abspath(os.path.join(current_directory, '..'))
sys.path.append(root_directory)

from logic.authorization_logic import User, check_password, create_user, get_hashed_password, hash_password

auth_bp = Blueprint('auth', __name__)

login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']

        hashed_password = hash_password(password)

        if create_user(login, hashed_password):
            return redirect('/login')
        else:
            error_message = 'Произошла ошибка. Пожалуйста, попробуйте снова.'
            return render_template('register.html', error=error_message)

    else:
        return render_template('auth/register.html')
    
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']

        hashed_password = get_hashed_password(login)

        if hashed_password and check_password(hashed_password, password):
            user = User(login)
            login_user(user)
            print("Успешный вход")
            user_info = {
                'login': current_user.get_id(),
                'is_admin': current_user.is_admin
            }
            print(user_info)
            return redirect('/')
        else:
            error_message = 'Неверные учетные данные. Пожалуйста, попробуйте снова.'
            return render_template('login.html', error=error_message)
    else:
        return render_template('auth/login.html')


@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))