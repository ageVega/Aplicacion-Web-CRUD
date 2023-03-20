# api.py
import os
from psycopg2 import connect, extras
from flask import Blueprint, jsonify, request
from flask_login import UserMixin
from flask_login import login_required

api = Blueprint('api', __name__)

# Accede a las variables de entorno
host = os.environ.get('DB_HOST')
port = os.environ.get('DB_PORT')
dbname = os.environ.get('DB_DATABASE')
username = os.environ.get('DB_USER')
password = os.environ.get('DB_PASSWORD')

def get_connection():
    conn = connect(host=host, port=port, dbname=dbname, user=username, password=password)
    return conn

# Clase de usuario para flask-login
class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

@api.route('/api/tasks', methods=['GET'])
@login_required
def get_tasks():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)

    cur.execute('SELECT * FROM tasks')
    tasks = cur.fetchall()

    cur.close()
    conn.close()

    return jsonify(tasks)

@api.route('/api/tasks', methods=['POST'])
@login_required
def create_task():
    new_task = request.get_json()
    task = new_task['task']
    priority = new_task['priority']

    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)

    cur.execute('INSERT INTO tasks (task, priority) VALUES (%s, %s) RETURNING *',
                (task, priority))

    new_created_task = cur.fetchone()
    conn.commit()

    cur.close()
    conn.close()

    return jsonify(new_created_task)

@api.route('/api/tasks/<int:id>', methods=['DELETE'])
@login_required
def delete_task(id):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)

    cur.execute('DELETE FROM tasks WHERE id = %s RETURNING *', (id,))
    task = cur.fetchone()

    conn.commit()

    cur.close()
    conn.close()

    if task is None:
        return jsonify({'message': 'Task not found'}), 404

    return jsonify(task)

@api.route('/api/tasks/<int:id>', methods=['PUT'])
@login_required
def update_task(id):
    new_task = request.get_json()
    task = new_task['task']
    priority = new_task['priority']

    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)

    cur.execute('UPDATE tasks SET task = %s, priority = %s WHERE id = %s RETURNING *',
                (task, priority, id))
    updated_task = cur.fetchone()

    conn.commit()

    cur.close()
    conn.close()

    if updated_task is None:
        return jsonify({'message': 'Task not found'}), 404

    return jsonify(updated_task)

@api.route('/api/tasks/<int:id>', methods=['GET'])
@login_required
def get_task(id):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)

    cur.execute('SELECT * FROM tasks WHERE id = %s', (id,))
    task = cur.fetchone()

    cur.close()
    conn.close()

    if task is None:
        return jsonify({'message': 'Task not found'}), 404

    return jsonify(task)


@api.route('/home')
@login_required
def home():
    return jsonify({"message": "Welcome to the home page"})