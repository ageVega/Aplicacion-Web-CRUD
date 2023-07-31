# Aplicacion-Web-CRUD

Este proyecto consiste en una aplicación web de gestión de tareas domésticas con una REST API en Flask, un frontend en Vanilla JavaScript y estilos aplicados mediante Bootstrap 5, todo ello desplegado en AWS mediante Terraform.

El frontend se desarrolla usando Vanilla JavaScript, lo que permite agregar, editar, eliminar y visualizar tareas con interacción del usuario. Se utiliza Bootstrap 5 para proporcionar estilos a la aplicación.

El backend se crea con el framework Flask de Python, e implementa una REST API para gestionar las tareas y la autenticación de usuarios basada en hogares. La base de datos empleada es PostgreSQL.

El proyecto también incluye un archivo Dockerfile para construir una imagen de Docker basada en Ubuntu y un archivo Terraform para desplegar la infraestructura en AWS.

El archivo Dockerfile define las variables de entorno necesarias para la conexión a la base de datos y expone el puerto 8080. También contiene scripts para instalar paquetes, clonar el repositorio del proyecto y ejecutar la aplicación.

La configuración de Terraform crea una VPC con subredes públicas y privadas, un grupo de seguridad, una plantilla de lanzamiento, un grupo de autoescalado, un Application Load Balancer con listeners para puertos 80 y 443, y un Target Group. Incluye variables para personalizar aspectos como la región de AWS entre otros.

Tutorial: https://www.youtube.com/watch?v=Qqgry8mezC8&t=7506s

# Iniciar aplicacion

1. Clonar repositorio

2. Copiar archivo .env

3. $ python -m src.app

4. Acceder a través de http://&lt;ip&gt;:8080

# Llamadas a la API

```bash
GET http://matrix.agevega.com/

GET http://localhost:5000/api/tasks

GET http://localhost:5000/api/tasks/<id>
```

```bash
POST http://localhost:5000/api/tasks 
{
 "task": "dummy",
 "priority": "1"
}
```

```bash
DELETE http://localhost:5000/api/tasks/<id>
```

```bash
PUT http://localhost:5000/api/tasks/<id>
{
 "task": "dummy",
 "priority": "2"
}
```

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
 
$ source venv/Scripts/activate
```

F1 --> Python: Select Interpreter --> .\venv\Scripts\python.exe --> New terminal

### Instalar modulos de python en entorno virtual

```bash
$ pip install flask

// Instalar postgres o $ sudo apt install libpq-dev

$ pip install psycopg2 // Libreria para comunicar nuestra aplicacion python con postgres

$ pip install cryptography

$ pip install python-dotenv

$ pip install waitress

$ pip install flask_login
```

### Instalar dependencias desde requirements.txt

```bash
$ pip install -r requirements.txt
```

### Generar requirements.txt

```bash
$ pip freeze > requirements.txt
```

# Despliegue en AWS

## EC2 Autoscaling group + Load Balancer

La aproximación que vamos a seguir pasa por: 

1. Crear una plantilla de lanzamiento desde la cual se puedan generar instancias EC2 con la aplicación operativa desde la creación de la propia instancia.

2. Crear un grupo de autoscaling que se encargue de mantener siempre un servidor healthy levantado a partir de nuestra plantilla de lanzamiento.
   
   1. Asociar un Target group a nuestro grupo de autoescalado.
   
   2. Apuntar con un Load Balancer a nuestro Target group para los protocolos HTTP y HTTPS (con certificado SSL/TLS).

3. Registrar un dominio y asociar un DNS al endpoint del Load Balancer.

### VPC

| Creación y configuración de VPC        | ****                                         |
| -------------------------------------- | -------------------------------------------- |
| Etiqueta Nombre                        | Matrix                                       |
| Bloque de CIDR IPv4                    | 10.X.0.0/16                                  |
| Número de zonas de disponibilidad (AZ) | 3                                            |
| Cantidad de subredes públicas          | 3                                            |
| Cantidad de subredes privadas          | 3                                            |
| ****                                   | ****                                         |
| **VPC**                                | **Su red virtual de AWS**                    |
| ****                                   | Matrix-vpc                                   |
| **Subredes (6)**                       | **Subredes dentro de esta VPC**              |
| eu-west-1a                             | Matrix-subnet-public1-eu-west-1a             |
| eu-west-1a                             | Matrix-subnet-private1-eu-west-1a            |
| eu-west-1b                             | Matrix-subnet-public2-eu-west-1b             |
| eu-west-1b                             | Matrix-subnet-private2-eu-west-1b            |
| eu-west-1c                             | Matrix-subnet-public3-eu-west-1c             |
| eu-west-1c                             | Matrix-subnet-private3-eu-west-1c            |
| **Tablas de enrutamiento (4)**         | **Dirigir el tráfico de red a los recursos** |
| Public subnets                         | Matrix-rtb-public                            |
| Private subnet 1                       | Matrix-rtb-private1-eu-west-1a               |
| Private subnet 2                       | Matrix-rtb-private2-eu-west-1b               |
| Private subnet 3                       | Matrix-rtb-private3-eu-west-1c               |
| **Conexiones de red (2)**              | **Conexiones a otras redes**                 |
| Public subnets                         | Matrix-igw                                   |
| Private subnets                        | Matrix-vpce-s3                               |

### Grupo de seguridad

| Configuración del grupo de seguridad | ****                                                                          |
| ------------------------------------ | ----------------------------------------------------------------------------- |
| Nombre del grupo de seguridad        | Matrix                                                                        |
| Descripcion                          | Grupo de seguridad de pruebas que permite acceso total de entrada y de salida |
| VPC                                  | **Seleccionar una VPC existente**                                             |
| **Reglas de entrada**                | ****                                                                          |
| Todo el tráfico                      | Anywhere-IPv4                                                                 |
| **Reglas de salida**                 | ****                                                                          |
| Todo el tráfico                      | Anywhere-IPv4                                                                 |

### Plantilla de lanzamiento

| Configuración de la plantilla                | ****                                            |
| -------------------------------------------- | ----------------------------------------------- |
| Nombre de la plantilla de lanzamiento        | Matrix-AmoDeCasa                                |
| Descripción de la plantilla                  | Plantilla de instancias de aplicacion AmoDeCasa |
| Imagen de software (AMI)                     | Canonical, Ubuntu, 22.04 LTS                    |
| Tipo de servidor virtual (tipo de instancia) | t2.micro                                        |
| Par de claves (inicio de sesión)             | denver.pem                                      |
| **Configuraciones de Red**                   | ****                                            |
| Subred                                       | No incluir en la plantilla de lanzamiento       |
| Firewall (grupos de seguridad)               | **Matrix**                                      |
| **Configuración de Red Avanzada**            | **Agregue interfaz de red**                     |
| Asignar automáticamente la IP pública        | Habilitar                                       |
| ****                                         | ****                                            |
| Volúmenes de EBS                             | 1 volúmen(es): 8 GiB                            |
| **Detalles avanzados**                       | ****                                            |

**Datos de usuario**

```bash
#!/bin/bash
# UBUNTU PYTHON AMODECASA
sudo su -
cd /home/ubuntu
apt update
apt install python3-pip -y
apt-get install libpq-dev -y
export PATH=$PATH:/usr/bin/pg_config
apt-get install postgresql -y
git clone https://github.com/ageVega/Aplicacion-Web-CRUD.git
pip install -r Aplicacion-Web-CRUD/requirements.txt
cat << EOT >> Aplicacion-Web-CRUD/.env
DB_HOST=
DB_DATABASE=
DB_PORT=
DB_USER=
DB_PASSWORD=
SECRET_KEY=
EOT
python3 -m Aplicacion-Web-CRUD.src.app
```

### Grupo de Autoescalado

| Configuración del grupo de Auto Scaling      | ****                                         |
| -------------------------------------------- | -------------------------------------------- |
| Nombre del grupo de Auto Scaling             | Matrix-AmoDeCasa                             |
| Plantilla de lanzamiento                     | Matrix-AmoDeCasa                             |
| VPC                                          | Matrix-vpc                                   |
| Zonas de disponibilidad y subredes           | ****                                         |
| ****                                         | Matrix-subnet-public1-eu-west-1a             |
| ****                                         | Matrix-subnet-public2-eu-west-1b             |
| ****                                         | Matrix-subnet-public3-eu-west-1c             |
| Balance de carga                             | **Asociar a un nuevo balanceador de carga**  |
| Tipo de balanceador de carga                 | Application Load Balancer                    |
| Nombre del balanceador de carga              | Matrix-AmoDeCasa                             |
| Esquema del balanceador de carga             | Internet-facing                              |
| Agentes de escucha y direccionamiento        | HTTP / Puerto 8080                           |
| Direccionamiento predeterminado (reenviar a) | **Crear un grupo de destino (Target group)** |
| Nombre del grupo de destino nuevo            | Matrix-AmoDeCasa                             |
| Comprobaciones de estado                     | EC2 / ELB                                    |
| **Tamaño del grupo**                         | ****                                         |
| Capacidad deseada                            | 1                                            |
| Capacidad mínima                             | 1                                            |
| Capacidad máxima                             | 1                                            |

### Target Group

| Configuración del grupo de destino | **** |
| ---------------------------------- | ---- |
| Health check settings              | Edit |
| Protocol                           | HTTP |
| Path                               | /    |
| Port                               | 8080 |

### AWS Certificate Manager

| Solicitar certificado público SSL/TLS | ****                      |
| ------------------------------------- | ------------------------- |
| Nombre de dominio completo            | matrix.agevega.com        |
| **Nombre CNAME**                      | **Valor CNAME**           |
| hash.matrix.agevega.com.              | hash.acm-validations.aws. |

### Route 53 Añadir los registros CNAME

| Nombre del registro          | Tipo de registro | Valor                         |
| ---------------------------- | ---------------- | ----------------------------- |
| matrix.agevega.com           | CNAME            | **LoadBalancer Endpoint**     |
| **hash**.matrix.agevega.com. | CNAME            | **hash**.acm-validations.aws. |

### Load balancer

| Configuración del balanceador de carga | ****                                      |
| -------------------------------------- | ----------------------------------------- |
| **Listeners**                          | **Default routing rule**                  |
| HTTP:80                                | **Forward to:** Matrix-AmoDeCasa          |
| HTTPS:443                              | **Forward to:** Matrix-AmoDeCasa          |
| Secure listener settings               | HTTPS Only                                |
| Default SSL/TLS certificate            | matrix.agevega.com (Certificate ID: hash) |
| **Security**                           | Edit                                      |
| Security groups                        | Matrix                                    |

