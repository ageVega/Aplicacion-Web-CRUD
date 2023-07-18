# api.py
from .connection import get_connection
from psycopg2 import extras
from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user

# Define un Blueprint para la API. Un Blueprint es un conjunto de rutas que pueden ser registradas en una aplicación Flask.
api_blueprint = Blueprint('api', __name__)

# Devuelve todas las tareas
@api_blueprint.route('/tasks', methods=['GET'])
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
@api_blueprint.route('/tasks', methods=['POST'])
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
@api_blueprint.route('/tasks/<int:id>', methods=['GET'])
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
@api_blueprint.route('/tasks/<int:id>', methods=['PUT'])
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
@api_blueprint.route('/tasks/<int:id>', methods=['DELETE'])
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


# Devuelve todos los niveles de prioridad para una casa
@api_blueprint.route('/priority_levels', methods=['GET'])
@login_required
def get_priority_levels():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)
    cur.execute("SELECT * FROM priority_levels WHERE house_id = %s ORDER BY level", (current_user.id,))  # Añadir "ORDER BY level"

    priority_levels = cur.fetchall()

    cur.close()
    conn.close()

    return jsonify(priority_levels)

# Modifica un nivel de prioridad para una casa
@api_blueprint.route('/priority_levels/<int:id>', methods=['PUT'])
@login_required
def update_priority_level(id):
    new_priority_level = request.get_json()
    level = new_priority_level['level']
    name = new_priority_level['name']

    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)

    cur.execute('UPDATE priority_levels SET level = %s, name = %s WHERE id = %s AND house_id = %s RETURNING *',
                (level, name, id, current_user.id))
    updated_priority_level = cur.fetchone()

    conn.commit()

    cur.close()
    conn.close()

    if updated_priority_level is None:
        return jsonify({'message': 'Priority level not found'}), 404

    return jsonify(updated_priority_level)

# Devuelve los nombres de los niveles de prioridad para una casa
@api_blueprint.route('/priority_names', methods=['GET'])
@login_required
def get_priority_names():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)
    cur.execute("SELECT * FROM priority_levels WHERE house_id = %s", (current_user.id,))

    priority_names = cur.fetchall()

    cur.close()
    conn.close()

    return jsonify(priority_names)

# Modifica el nombre de una prioridad para una casa
@api_blueprint.route('/priority_names/<int:level>', methods=['PUT'])
@login_required
def update_priority_name(level):
    new_priority_name = request.get_json()
    name = new_priority_name['name']

    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)

    cur.execute('UPDATE priority_levels SET name = %s WHERE level = %s AND house_id = %s RETURNING *',
                (name, level, current_user.id))
    updated_priority_name = cur.fetchone()

    conn.commit()

    cur.close()
    conn.close()

    if updated_priority_name is None:
        return jsonify({'message': 'Priority name not found'}), 404

    return jsonify(updated_priority_name)

@api_blueprint.route('/reset_priority_names', methods=['POST'])
@login_required
def reset_priority_names():
    default_priorities = [
        (1, 'Crítica'),
        (2, 'Urgente'),
        (3, 'Importante'),
        (4, 'Moderado'),
        (5, 'Menor'),
        (6, 'Trivial'),
        (7, 'Otro'),
    ]

    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)

    try:
        for level, name in default_priorities:
            cur.execute('UPDATE priority_levels SET name = %s WHERE level = %s AND house_id = %s',
                        (name, level, current_user.id))
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"Error resetting priority names: {str(e)}")
    finally:
        cur.close()
        conn.close()

    return get_priority_levels()

@api_blueprint.route('/set_weekday_priority_names', methods=['POST'])
@login_required
def set_weekday_priority_names():
    weekday_priorities = [
        (1, 'Lunes'),
        (2, 'Martes'),
        (3, 'Miércoles'),
        (4, 'Jueves'),
        (5, 'Viernes'),
        (6, 'Sábado'),
        (7, 'Domingo'),
    ]

    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)

    try:
        for level, name in weekday_priorities:
            cur.execute('UPDATE priority_levels SET name = %s WHERE level = %s AND house_id = %s',
                        (name, level, current_user.id))
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"Error setting weekday priority names: {str(e)}")
    finally:
        cur.close()
        conn.close()

    return get_priority_levels()
