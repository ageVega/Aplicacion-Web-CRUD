# Aplicacion-Web-CRUD

Ejemplo práctico en el que crearemos una web completa usando Python y JavaScript. Crearemos un Backend usando el Framework de Python Flask y el frontend lo crearemos usando Javascript puro (Vanilla Javascript) desde cero. Básicamente crearemos una REST API, más un frontend, y lo estilizaremos con bootstrap5.

Tutorial: https://www.youtube.com/watch?v=Qqgry8mezC8&t=7506s

# Iniciar aplicacion

- Clonar repositorio

- Copiar archivo .env

- $ python app.py

- Acceder a traves de http://<ip>:8080

# Instalacion de entorno

## Version de python

### Comprobar version de python y pip

```bash
$ python --version
Python 3.10.4
```

```bash
$ pip --version
pip 22.3.1 from C:\Users\ageve\AppData\Local\Programs\Python\Python310\lib\site-packages\pip (python 3.10)
```

### Instalar pip

```bash
sudo apt update

sudo apt install python3-pip
```

## Crear entorno virtual

### Instalar y crear virtualenv

```bash
$ pip install virtualenv

$ python -m virtualenv venv

F1 --> Python: Select Interpreter --> .\venv\Scripts\python.exe --> New terminal
```

### Instalar modulos de python en entorno virtual

```bash
$ pip install flask

Instalar postgres o $ sudo apt install libpq-dev

$ pip install psycopg2 // Libreria para comunicar nuestra aplicacion python con postgres

$ pip install psycopg2-binary

$ pip install cryptography

$ pip install python-dotenv

$ pip install gunicorn

$ pip install waitress
```

### Instalar dependencias desde requirements.txt

```bash
$ pip install -r requirements.txt
```

### Generar requirements.txt

```bash
$ pip freeze > requirements.txt
```

# Llamadas a la API

> POST [http://localhost:5000/api/users](http://localhost:5000/api/users) {
>  "username": "Agevega",
>  "email": "[agevega@gmail.com](mailto:agevega@gmail.com)",
>  "password": "erculotuyo13"
> }



# Despliegue en AWS


