from flask import Flask
from psycopg2 import connect

app = Flask(__name__)

host = 'localhost'
port = 5432
dbname = 'usersdb'
username = 'postgres'
password = '1234'

def get_connection():
    conn = connect(host=host, port=port, dbname=dbname, user=username, password=password)
    return conn

@app.get('/api/users')
def get_users():
    return 'getting users'

@app.post('/api/users')
def create_user():
    return 'creating users'

@app.delete('/api/users/1')
def delete_user():
    return 'deleting users'

@app.put('/api/users/1')
def update_user():
    return 'updating users'

@app.get('/api/users/1')
def get_user():
    return 'getting user 1'


if __name__ == '__main__':
    app.run(debug=True)
