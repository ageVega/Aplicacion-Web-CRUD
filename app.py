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

@app.get('/')
def home():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT 1 + 1")
    result = cur.fetchone()

    print(result)
    return 'Hello World!'

if __name__ == '__main__':
    app.run(debug=True)
