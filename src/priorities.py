# api.py
from .connection import get_connection
from psycopg2 import extras
from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user

# Define un Blueprint para la API. Un Blueprint es un conjunto de rutas que pueden ser registradas en una aplicación Flask.
priorities_blueprint = Blueprint('priorities', __name__)

# Devuelve todos los niveles de prioridad para una casa
@priorities_blueprint.route('/priority_names', methods=['GET'])
@login_required
def get_priority_names():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)

    cur.execute("SELECT * FROM priority_levels WHERE house_id = %s ORDER BY level", (current_user.id,))
    priority_names = cur.fetchall()

    cur.close()
    conn.close()

    return jsonify(priority_names)

# Modifica el nombre de una prioridad para una casa
@priorities_blueprint.route('/priority_names/<int:level>', methods=['PUT'])
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

# Establece los valores de prioridad por defecto
@priorities_blueprint.route('/reset_priority_names', methods=['POST'])
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

    return get_priority_names()

# Establece los valores de prioridad vacíos
@priorities_blueprint.route('/set_empty_priority_names', methods=['POST'])
@login_required
def set_empty_priority_names():
    weekday_priorities = [
        (1, ' '),
        (2, ' '),
        (3, ' '),
        (4, ' '),
        (5, ' '),
        (6, ' '),
        (7, ' '),
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
        print(f"Error setting empty priority names: {str(e)}")
    finally:
        cur.close()
        conn.close()

    return get_priority_names()

# Establece los valores de prioridad a los dias de la semana
@priorities_blueprint.route('/set_weekday_priority_names', methods=['POST'])
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

    return get_priority_names()
