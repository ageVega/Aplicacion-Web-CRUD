# api.py
from .connection import get_connection
from psycopg2 import extras
from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user

# Define un Blueprint para la API. Un Blueprint es un conjunto de rutas que pueden ser registradas en una aplicación Flask.
api_blueprint = Blueprint('api', __name__)

# Devuelve todas las tareas
@api_blueprint.route('/api/tasks', methods=['GET'])
@login_required
def get_tasks():
    house_id = request.args.get('house_id')
    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)
    cur.execute("SELECT * FROM tasks WHERE house_id = %s", (current_user.id,))

    tasks = cur.fetchall()

    cur.close()
    conn.close()

    return jsonify(tasks)

# Crea una nueva tarea
@api_blueprint.route('/api/tasks', methods=['POST'])
@login_required
def create_task():
    new_task = request.get_json()
    task = new_task['task']
    priority = new_task['priority']
    house_id = new_task['house_id']

    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)
    cur.execute("INSERT INTO tasks (task, priority, house_id) VALUES (%s, %s, %s) RETURNING *", (task, priority, current_user.id))
    new_created_task = cur.fetchone()
    conn.commit()

    cur.close()
    conn.close()

    return jsonify(new_created_task)

# Devuelve una tarea existente
@api_blueprint.route('/api/tasks/<int:id>', methods=['GET'])
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

# Modifica una tarea existente
@api_blueprint.route('/api/tasks/<int:id>', methods=['PUT'])
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

# Borra una tarea existente
@api_blueprint.route('/api/tasks/<int:id>', methods=['DELETE'])
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
