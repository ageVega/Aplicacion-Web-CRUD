# house.py
from .connection import get_connection
from psycopg2 import extras
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

# Definición de la clase House
class House(UserMixin):
    def __init__(self, id, house_name, password):
        self.id = id
        self.house_name = house_name
        self.password = password
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


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

def create_house(house_name, password):
    hashed_password = generate_password_hash(password)

    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)

    try:
        cur.execute('INSERT INTO houses (house_name, password) VALUES (%s, %s) RETURNING id, house_name, password', 
                    (house_name, hashed_password))
        house_data = cur.fetchone()
        conn.commit()
    except Exception as e:
        conn.rollback()
        return None, str(e)

    cur.close()
    conn.close()

    return House(house_data['id'], house_data['house_name'], house_data['password']), None
