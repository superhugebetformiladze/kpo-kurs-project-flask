from flask import Flask
from website.client.routes.client_routes import client_bp

app = Flask(__name__)

app.register_blueprint(client_bp)

if __name__ == '__main__':
    app.run(debug=True)
