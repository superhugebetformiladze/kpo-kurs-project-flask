from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import login_required
from werkzeug.utils import secure_filename

import sys
import os

current_directory = os.path.dirname(os.path.realpath(__file__))
root_directory = os.path.abspath(os.path.join(current_directory, ".."))
sys.path.append(root_directory)

from website.client.logic.service_logic import read_service_by_id, read_services
from logic.admin_logic import create_service, delete_service, is_admin, update_service

admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/admin")
@login_required
def admin_home():
    if not is_admin():
        print("Нет доступа в админ панель")
        return redirect(url_for("client.index"))
    current_page = "admin"
    return render_template("admin/admin-home.html", current_page=current_page)


@admin_bp.route("/admin/services")
@login_required
def admin_services():
    if not is_admin():
        print("Нет доступа в админ панель")
        return redirect(url_for("client.index"))
    current_page = "products"
    services = read_services()
    return render_template(
        "admin/admin-services.html", services=services, current_page=current_page
    )


@admin_bp.route("/admin/service", methods=["POST", "GET"])
@login_required
def admin_create_service():
    if not is_admin():
        print("Нет доступа в админ панель")
        return redirect(url_for("client.index"))
    if request.method == "POST":
        service_name = request.form["service_name"]
        description = request.form["description"]
        additional_info = request.form["additional_info"]
        price = request.form["price"]

        uploaded_file = request.files["image"]

        if uploaded_file:
            # Компонование пути к файлу
            image_filename = secure_filename(uploaded_file.filename)
            image_path = os.path.join(
                "static", "images", "client", "services", service_name, image_filename
            )

            # Создание папок, если они не существуют
            os.makedirs(os.path.dirname(image_path), exist_ok=True)

            # Сохранение файла
            uploaded_file.save(image_path)
            image_path = "/" + image_path  # Добавляем слеш перед static
        else:
            image_path = ""  # Если файл не был загружен, можно установить пустой путь

        service_data = {
            "service_name": service_name,
            "description": description,
            "additional_info": additional_info,
            "price": price,
            "image": image_path,
        }

        if create_service(service_data):
            return redirect(url_for("admin.admin_services"))

    elif request.method == "GET":
        return render_template("admin/admin-service-edit.html")
    return abort(500)


@admin_bp.route("/admin/service/delete/<int:service_id>", methods=["GET"])
@login_required
def admin_delete_service(service_id):
    if not is_admin():
        print("Нет доступа в админ панель")
        return redirect(url_for("client.index"))
    delete_service(service_id)
    return redirect(url_for("admin.admin_services"))


@admin_bp.route("/admin/service/edit/<int:service_id>", methods=["GET", "POST"])
@login_required
def admin_edit_service(service_id):
    if not is_admin():
        print("Нет доступа в админ панель")
        return redirect(url_for("client.index"))
    edit_mode = True
    service_data = read_service_by_id(service_id)

    if request.method == "POST":
        service_name = request.form["service_name"]
        description = request.form["description"]
        additional_info = request.form["additional_info"]
        price = request.form["price"]

        uploaded_file = request.files["image"]

        if uploaded_file:
            # Компонование пути к файлу
            image_filename = secure_filename(uploaded_file.filename)
            new_image_path = os.path.join(
                "static", "images", "main-page", service_name, image_filename
            )

            # Удаление старой картинки, если она существует
            if os.path.exists(service_data[4]):
                try:
                    os.remove(service_data[4])
                except OSError as e:
                    print("Error: %s - %s." % (e.filename, e.strerror))

            # Создание папок, если они не существуют
            os.makedirs(os.path.dirname(new_image_path), exist_ok=True)

            # Сохранение новой картинки
            uploaded_file.save(new_image_path)
            image_path = "/" + new_image_path

        else:
            image_path = service_data[4]

        service_data_updated = {
            "service_name": service_name,
            "description": description,
            "additional_info": additional_info,
            "price": price,
            "image": image_path,
        }

        update_service(service_id, service_data_updated)
        return redirect(url_for("admin.admin_services"))

    return render_template(
        "admin/admin-service-edit.html", edit_mode=edit_mode, service_data=service_data
    )
