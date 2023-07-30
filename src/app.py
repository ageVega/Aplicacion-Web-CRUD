# app.py
from .login import login_blueprint, login_manager
from .api import tasks_blueprint
from .priorities import priorities_blueprint
from os import environ
from dotenv import load_dotenv
from flask import Flask, session, render_template, redirect, url_for
from flask_login import current_user, login_required

load_dotenv()  # Carga las variables de entorno desde .env

app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.secret_key = environ.get('SECRET_KEY')  # Se utiliza para cifrar las cookies de sesión del usuario, Flask-Login utiliza estas cookies para recordar a los usuarios entre solicitudes.

app.register_blueprint(login_blueprint, url_prefix='/auth')
app.register_blueprint(tasks_blueprint, url_prefix='/api')
app.register_blueprint(priorities_blueprint, url_prefix='/priorities')

login_manager.init_app(app)
login_manager.login_view = "auth.login"  # Establece la vista de inicio de sesión


@app.route('/')
def index():
    return redirect(url_for('home'))

@app.route('/home')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('home.html')

@app.route('/dashboard')
@login_required
def dashboard():
    house_name = session.get('house_name', 'Invitado')
    return render_template('dashboard.html', house_name=house_name)

@app.route('/priority_names')
@login_required
def priority_names():
    house_name = session.get('house_name', 'Invitado')
    return render_template('priority_names.html', house_name=house_name)

@app.route('/config')
@login_required
def config():
    house_name = session.get('house_name', 'Invitado')
    return render_template('config.html', house_name=house_name)


if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)

"""
if __name__ == '__main__':
    app.run(debug=True)

"""
