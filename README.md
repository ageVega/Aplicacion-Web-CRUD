# Aplicacion-Web-CRUD
Ejemplo práctico en el que crearemos una web completa usando Python y JavaScript. Crearemos un Backend usando el Framework de Python Flask y el frontend lo crearemos usando Javascript puro (Vanilla Javascript) desde cero. Básicamente crearemos una REST API, más un frontend, y lo estilizaremos con bootstrap5.

Tutorial: https://www.youtube.com/watch?v=Qqgry8mezC8&t=7506s

# Notas

## Comprobar version de python y pip

$ python --version
Python 3.10.4

$ pip --version
pip 22.3.1 from C:\Users\ageve\AppData\Local\Programs\Python\Python310\lib\site-packages\pip (python 3.10)

## Crear entorno virtual 

$ pip install virtualenv

$ python -m virtualenv venv

F1 --> Python: Select Interpreter --> .\venv\Scripts\python.exe --> New terminal

## Instalar modulos de python en entorno virtual 

$ pip install flask

Instalar postgres o $ sudo apt install libpq-dev

$ pip install psycopg2 // Libreria para comunicar nuestra aplicacion python con postgres

$ pip install cryptography

$ pip install python-dotenv

$ pip install gunicorn

## Llamadas a la API

POST http://localhost:5000/api/users
{
  "username": "Agevega",
  "email": "agevega@gmail.com",
  "password": "erculotuyo13"
}

## Generar requirements.txt

$ pip freeze > requirements.txt

## Instalar dependencias

$ pip install -r requirements.txt