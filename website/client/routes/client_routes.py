from flask import Blueprint, render_template
import random

import sys
import os
current_directory = os.path.dirname(os.path.realpath(__file__))
root_directory = os.path.abspath(os.path.join(current_directory, '..'))
sys.path.append(root_directory)

from logic.service_logic import read_all_services_exclude, read_services, read_service_by_id

client_bp = Blueprint('client', __name__)

@client_bp.route('/')
def index():
    all_services = read_services()

    if len(all_services) >= 3:
        random_services = random.sample(all_services, 3)
    else:
        random_services = all_services

    return render_template('client/index.html', services=random_services)

@client_bp.route('/service/<int:service_id>')
def service_detail(service_id):
    service = read_service_by_id(service_id)
    all_services = read_all_services_exclude(service_id)
    if len(all_services) >= 3:
        random_services = random.sample(all_services, 3)
    else:
        random_services = all_services
    return render_template('client/service-detail.html', service=service, services=random_services)

@client_bp.route('/services')
def services():
    all_services = read_services()
    return render_template('client/services.html', services=all_services)

