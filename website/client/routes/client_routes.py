from flask import Blueprint, render_template

import sys
import os
current_directory = os.path.dirname(os.path.realpath(__file__))
root_directory = os.path.abspath(os.path.join(current_directory, '..'))
sys.path.append(root_directory)

from logic.service_logic import read_services, read_service_by_id

client_bp = Blueprint('client', __name__)

@client_bp.route('/')
def index():
    services = read_services()
    return render_template('client/index.html', services=services)

@client_bp.route('/service/<int:service_id>')
def service_detail(service_id):
    service = read_service_by_id(service_id)
    return render_template('service_detail.html', service=service)
