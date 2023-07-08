# login.py
from .connection import get_connection
from .house import House, get_house_by_id, get_house_by_house_name, create_house
from psycopg2 import extras
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash

# Crea una instancia de LoginManager, que maneja el proceso de autenticación de usuarios.
login_manager = LoginManager()

@login_manager.user_loader # Esto es un decorador que flask_login utiliza para cargar una casa
def load_user(house_id):
    return get_house_by_id(house_id)

# Define un Blueprint para la API. Un Blueprint es un conjunto de rutas que pueden ser registradas en una aplicación Flask.
login_blueprint = Blueprint('auth', __name__)

# Si la solicitud es POST, procesa la información del formulario de registro. Si es GET, devuelve la página del formulario.
@login_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        house_name = request.form.get('house_name').lower()  # Convertir a minúsculas
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password != confirm_password:
            flash("Las contraseñas no coinciden. Por favor, inténtalo de nuevo.", "danger")
            return redirect(url_for('auth.register_form'))

        house, error = create_house(house_name, password)
        if error:
            return jsonify({'message': error}), 400

        return redirect(url_for('home'))  # Redirige a la ruta principal al registrarse
    else:
        return render_template('register.html')

# Si la solicitud es POST, procesa la información del formulario de login. Si es GET, devuelve la página del formulario.
@login_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    if request.method == 'POST':
        house_name = request.form['house_name'].lower()  # Convertir a minúsculas
        password = request.form['password']
        house = get_house_by_house_name(house_name)
        session['house_id'] = house['id']

        if house and check_password_hash(house['password'], password):
            house_obj = House(house['id'], house['house_name'], house['password'])
            login_user(house_obj)
            capitalized_house_name = house['house_name'].capitalize() # Asegurar que el nombre de la casa empiece con mayúscula
            session['house_name'] = capitalized_house_name  # Guarda el nombre de la casa en la sesión
            return redirect(url_for('dashboard'))
        else:
            flash('Nombre de casa o contraseña incorrectos.')
    else:
        return render_template('login.html')

@login_blueprint.route('/logout')
@login_required
def logout():
    session.pop('house_id', None)
    session.pop('house_name', None)
    logout_user()
    return redirect(url_for('home'))
