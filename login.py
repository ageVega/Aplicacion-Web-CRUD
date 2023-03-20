# login.py
from flask import Blueprint, request, redirect, url_for, jsonify, render_template
from psycopg2 import connect, extras
from os import environ
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required

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

class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

def get_user_by_id(user_id):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)

    cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user_data = cur.fetchone()

    cur.close()
    conn.close()

    if user_data:
        return User(user_data['id'], user_data['username'], user_data['password'])

    return None

@login_manager.user_loader
def load_user(user_id):
    return get_user_by_id(user_id)

@login_blueprint.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')

    hashed_password = generate_password_hash(password)

    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)

    try:
        cur.execute('INSERT INTO users (username, password) VALUES (%s, %s) RETURNING id, username', (username, hashed_password))
        user_data = cur.fetchone()
        conn.commit()
    except Exception as e:
        conn.rollback()
        return jsonify({'message': str(e)}), 400

    cur.close()
    conn.close()

    user = User(user_data['id'], user_data['username'], hashed_password)
    login_user(user)
    return redirect(url_for('home'))  # Redirige a la ruta principal al registrarse

@login_blueprint.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)

    cur.execute('SELECT * FROM users WHERE username = %s', (username,))
    user_data = cur.fetchone()

    cur.close()
    conn.close()

    if not user_data or not check_password_hash(user_data['password'], password):
        return jsonify({'message': 'Invalid username or password'}), 401

    user = User(user_data['id'], user_data['username'], user_data['password'])
    login_user(user)
    return redirect(url_for('home'))  # Redirige a la ruta principal al iniciar sesión

@login_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@login_blueprint.route('/register', methods=['GET'])
def register_form():
    return render_template('register.html')

@login_blueprint.route('/login', methods=['GET'])
def login_form():
    return render_template('login.html')
