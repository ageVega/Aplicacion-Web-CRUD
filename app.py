# app.py
import os
from dotenv import load_dotenv
from flask import Flask, send_file
from api import api

load_dotenv()  # Carga las variables de entorno desde .env

app = Flask(__name__)
app.register_blueprint(api)

@app.route('/')
def home():
    return send_file('static/index.html')

if __name__ == '__main__':
    app.run(debug=True)
