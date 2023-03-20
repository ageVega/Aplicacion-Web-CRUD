# login.py
import os
from psycopg2 import connect, extras
from flask import Blueprint, request, redirect, url_for, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, UserMixin

login_blueprint = Blueprint('login', __name__)

# Accede a las variables de entorno
host = os.environ.get('DB_HOST')
port = os.environ.get('DB_PORT')
dbname = os.environ.get('DB_DATABASE')
username = os.environ.get('DB_USER')
password = os.environ.get('DB_PASSWORD')

def get_connection():
    conn = connect(host=host, port=port, dbname=dbname, user=username, password=password)
    return conn

class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

def get_user(user_id):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)
    cur.execute('SELECT * FROM users WHERE id = %s', (user_id,))
    user_data = cur.fetchone()
    cur.close()
    conn.close()

    if user_data:
        return User(user_data['id'], user_data['username'], user_data['password'])
    else:
        return None

@login_blueprint.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    hashed_password = generate_password_hash(password)

    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)
    cur.execute('INSERT INTO users (username, password) VALUES (%s, %s) RETURNING id', (username, hashed_password))
    user_id = cur.fetchone()['id']
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"id": user_id, "username": username})

@login_blueprint.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)
    cur.execute('SELECT * FROM users WHERE username = %s', (username,))
    user_data = cur.fetchone()
    cur.close()
    conn.close()

    if user_data and check_password_hash(user_data['password'], password):
        user = User(user_data['id'], user_data['username'], user_data['password'])
        login_user(user)
        return redirect(url_for('api.get_tasks'))
    else:
        return jsonify({"error": "Invalid username or password"}), 401

@login_blueprint.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('api.home'))
