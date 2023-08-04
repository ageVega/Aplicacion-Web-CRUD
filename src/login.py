# login.py
from .connection import get_connection
from .house import House, get_house_by_id, get_house_by_house_name, create_house, update_password
from psycopg2 import extras
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

# Crea una instancia de LoginManager, que maneja el proceso de autenticación de usuarios.
login_manager = LoginManager()

@login_manager.user_loader # Esto es un decorador que flask_login utiliza para cargar una casa
def load_user(house_id):
    return get_house_by_id(house_id)

# Define un Blueprint para la API. Un Blueprint es un conjunto de rutas que pueden ser registradas en una aplicación Flask.
login_blueprint = Blueprint('auth', __name__)

@login_blueprint.route('/change_password', methods=['POST'])
@login_required
def change_password():
    # Obtén las contraseñas desde el formulario
    old_password = request.form.get('oldPassword')
    new_password = request.form.get('newPassword')
    confirm_password = request.form.get('confirmPassword')

    # Validación de entrada
    if not old_password or not new_password or not confirm_password:
        flash('Por favor, introduce las contraseñas', 'danger')
        return redirect(url_for('change_password'))

    # Verifica que la nueva contraseña y la confirmación coinciden
    if new_password != confirm_password:
        flash("Las contraseñas no coinciden. Por favor, inténtalo de nuevo.", "danger")
        return redirect(url_for('change_password'))

    # Obtén el usuario actual desde la base de datos
    house = get_house_by_id(session['house_id'])

    # Manejo de errores si la casa no existe
    if house is None:
        flash('Error inesperado. Inténtalo de nuevo.', 'danger')
        return redirect(url_for('change_password'))

    # Verifica si la contraseña antigua es correcta
    if check_password_hash(house.password, old_password):
        # Verificar que la nueva contraseña no sea igual a la antigua
        if check_password_hash(house.password, new_password):
            flash('La nueva contraseña debe ser diferente a la antigua', 'danger')
            return redirect(url_for('change_password'))

        # Si la contraseña antigua es correcta, actualiza la contraseña
        hashed_password = generate_password_hash(new_password)

        # Aquí asumimos que tienes una función update_password que actualiza la contraseña del usuario en la base de datos
        update_password(session['house_id'], hashed_password)

        flash('La contraseña ha sido cambiada con éxito', 'success')
        return redirect(url_for('dashboard'))
    else:
        # Si la contraseña antigua es incorrecta, muestra un mensaje de error
        flash('La contraseña antigua es incorrecta', 'danger')
        return redirect(url_for('change_password'))

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

        return redirect(url_for('home'))  # Redirige a la página principal al registrarse
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

        if house:
            if check_password_hash(house['password'], password):
                session['house_id'] = house['id']
                house_obj = House(house['id'], house['house_name'], house['password'])
                login_user(house_obj)
                capitalized_house_name = house['house_name'].capitalize()  # Asegurar que el nombre de la casa empiece con mayúscula
                session['house_name'] = capitalized_house_name  # Guarda el nombre de la casa en la sesión
                return redirect(url_for('dashboard'))
            else:
                flash('Contraseña incorrecta.')
        else:
            flash('Esta casa no existe.')
        
        return render_template('login.html')  # Devuelve la página de login si la autenticación falla

    else:
        return render_template('login.html')  # Devuelve la página de login si la solicitud es GET


@login_blueprint.route('/logout')
@login_required
def logout():
    session.pop('house_id', None)
    session.pop('house_name', None)
    logout_user()
    return redirect(url_for('home'))

@login_blueprint.route('/cancel/<int:house_id>', methods=['DELETE'])
@login_required
def delete_house(house_id):
    if house_id != current_user.id:
        return jsonify({'message': 'No puedes eliminar otra casa'}), 400

    conn = get_connection()
    cursor = conn.cursor(cursor_factory=extras.RealDictCursor)
    try:
        cursor.execute("DELETE FROM houses WHERE id = %s", (house_id,))
        conn.commit()
    except Exception as e:
        conn.rollback()
        return jsonify({'message': 'Error al eliminar la casa'}), 500
    finally:
        cursor.close()
        conn.close()

    logout_user()
    return jsonify({'message': 'Casa eliminada correctamente'}), 200
