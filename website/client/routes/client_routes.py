import asyncio
from flask import Blueprint, redirect, render_template, request, url_for
import random

import sys
import os

from flask_login import current_user, login_required
from telegram import Bot


current_directory = os.path.dirname(os.path.realpath(__file__))
root_directory = os.path.abspath(os.path.join(current_directory, ".."))
sys.path.append(root_directory)

from logic.service_logic import (
    read_all_services_exclude,
    read_services,
    read_service_by_id,
)
from utils.config_utils import get_telegram_config

client_bp = Blueprint("client", __name__)

telegram_config = get_telegram_config()
bot = Bot(token=telegram_config['bot_token'])
chat_id = telegram_config['chat_id']

@client_bp.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        client_name = request.form["client_name"]
        car_brand = request.form["car_brand"]
        car_model = request.form["car_model"]
        service_name = request.form["service_name"]
        phone_number = request.form["phone_number"]
        message_text = f"Новая заявка!\n\n" \
                        f"Имя: {client_name}\n" \
                        f"Марка автомобиля: {car_brand}\n" \
                        f"Модель автомобиля: {car_model}\n" \
                        f"Услуга: {service_name}\n" \
                        f"Номер телефона: {phone_number}"
        
        print("chat id:",chat_id)
        print("bot:", bot)
        print("token:", telegram_config['bot_token'])
        print("message text:", message_text)

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(bot.send_message(chat_id, message_text))
                    
        return redirect(url_for("client.index"))
    else:
        all_services = read_services()

        if len(all_services) >= 3:
            random_services = random.sample(all_services, 3)
        else:
            random_services = all_services

    return render_template("client/index.html", services=random_services)


@client_bp.route("/service/<int:service_id>")
def service_detail(service_id):
    service = read_service_by_id(service_id)
    all_services = read_all_services_exclude(service_id)
    if len(all_services) >= 3:
        random_services = random.sample(all_services, 3)
    else:
        random_services = all_services
    return render_template(
        "client/service-detail.html", service=service, services=random_services
    )


@client_bp.route("/services")
def services():
    all_services = read_services()
    return render_template("client/services.html", services=all_services)


@client_bp.route("/profile")
@login_required
def profile():
    user_info = {
        "id": current_user.get_id(),
        "login": current_user.login,
        "role": current_user.role,
    }
    return render_template("client/profile.html", user_info=user_info)
