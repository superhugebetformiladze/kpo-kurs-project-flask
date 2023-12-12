from flask import Flask
from website.client.routes.client_routes import client_bp
from website.admin.routes.admin_routes import admin_bp
from website.authorization.routes.authorization_routes import auth_bp, login_manager

import sys
import os
current_directory = os.path.dirname(os.path.realpath(__file__))
root_directory = os.path.abspath(os.path.join(current_directory, '..'))
sys.path.append(root_directory)

from utils.config_utils import get_app_config

app = Flask(__name__)

app_config = get_app_config()
app.secret_key = app_config['secret_key']

login_manager.init_app(app)

app.register_blueprint(client_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(auth_bp)

if __name__ == '__main__':
    app.run(debug=True)
