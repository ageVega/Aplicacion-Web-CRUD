# app.py
import os
from dotenv import load_dotenv
from flask import Flask, send_file
from flask_login import LoginManager, current_user
from api import api
from login import login_blueprint
from login import login_manager  # Importa la instancia de LoginManager desde login.py

load_dotenv()  # Carga las variables de entorno desde .env

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')  # Necesario para flask-login
app.register_blueprint(api)
app.register_blueprint(login_blueprint, url_prefix='/auth')

# login_manager = LoginManager()  # Elimina la creación de una segunda instancia
login_manager.init_app(app)
login_manager.login_view = "auth.login"  # Establece la vista de inicio de sesión

@app.route('/')
def home():
    return send_file('static/index.html')

if __name__ == '__main__':
    app.run(debug=True)
