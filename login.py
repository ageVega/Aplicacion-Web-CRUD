# login.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from psycopg2 import connect, extras
from os import environ
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required, current_user

load_dotenv()  # Carga las variables de entorno desde .env

login_blueprint = Blueprint('auth', __name__)

host = environ.get('DB_HOST')
port = environ.get('DB_PORT')
dbname = environ.get('DB_DATABASE')
username = environ.get('DB_USER')
password = environ.get('DB_PASSWORD')

login_manager = LoginManager()

def get_connection():
    conn = connect(host=host, port=port, dbname=dbname, user=username, password=password)
    return conn

class House(UserMixin):
    def __init__(self, id, house_name, password):
        self.id = id
        self.house_name = house_name
        self.password = password

def get_house_by_id(house_id):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)

    cur.execute("SELECT * FROM houses WHERE id = %s", (house_id,))
    house_data = cur.fetchone()

    cur.close()
    conn.close()

    if house_data:
        return House(house_data['id'], house_data['house_name'], house_data['password'])

    return None

def get_house_by_house_name(house_name):
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=extras.DictCursor)
    cursor.execute("SELECT * FROM houses WHERE house_name = %s", (house_name,))
    house = cursor.fetchone()
    cursor.close()
    conn.close()
    return house


@login_manager.user_loader
def load_user(house_id):
    return get_house_by_id(house_id)


@login_blueprint.route('/register', methods=['POST'])
def register():
    house_name = request.form.get('house_name').lower()  # Convertir a minúsculas
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')

    if password != confirm_password:
        flash("Las contraseñas no coinciden. Por favor, inténtalo de nuevo.", "danger")
        return redirect(url_for('auth.register_form'))

    hashed_password = generate_password_hash(password)

    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)

    try:
        cur.execute('INSERT INTO houses (house_name, password) VALUES (%s, %s) RETURNING id, house_name', (house_name, hashed_password))
        house_data = cur.fetchone()
        conn.commit()
    except Exception as e:
        conn.rollback()
        return jsonify({'message': str(e)}), 400

    cur.close()
    conn.close()

    return redirect(url_for('home'))  # Redirige a la ruta principal al registrarse

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

    return render_template('login.html')

@login_blueprint.route('/logout')
@login_required
def logout():
    session.pop('house_id', None)
    session.pop('house_name', None)
    logout_user()
    return redirect(url_for('home'))

@login_blueprint.route('/register', methods=['GET'])
def register_form():
    return render_template('register.html')

@login_blueprint.route('/login', methods=['GET'])
def login_form():
    return render_template('login.html')
