# app.py
import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template
from flask_login import LoginManager, current_user, login_required
from api import api
from login import login_blueprint
from login import login_manager  # Importa la instancia de LoginManager desde login.py
from flask import session

load_dotenv()  # Carga las variables de entorno desde .env

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')  # Necesario para flask-login
app.register_blueprint(api)
app.register_blueprint(login_blueprint, url_prefix='/auth')

login_manager.init_app(app)
login_manager.login_view = "auth.login"  # Establece la vista de inicio de sesión


@app.route('/')
@login_required  # Asegura que sólo los usuarios autenticados puedan acceder a esta ruta
def home():
    username = session.get('username', 'Invitado')
    return render_template('index.html', username=username)


if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)

"""
if __name__ == '__main__':
    app.run(debug=True)
"""
