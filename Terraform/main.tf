
# VARIABLES
# --------------------------------------

variable "aws_region" {
  default = "eu-west-1"
}

variable "vpc_name" {
  default = "Matrix"
}

variable "vpc_cidr" {
  default = "10.0.0.0/16"
}

variable "public_subnets" {
  default = {
    "eu-west-1a" = "10.0.0.0/20"
    "eu-west-1b" = "10.0.16.0/20"
    "eu-west-1c" = "10.0.32.0/20"
  }
}

variable "private_subnets" {
  default = {
    "eu-west-1a" = "10.0.128.0/20"
    "eu-west-1b" = "10.0.144.0/20"
    "eu-west-1c" = "10.0.160.0/20"
  }
}

variable "ami_id" {
  default = "ami-00aa9d3df94c6c354" # Ubuntu Server 22.04 LTS, actualiza este valor si es necesario
}

variable "instance_type" {
  default = "t2.micro"
}

variable "key_pair" {
  default = "denver.pem"
}

variable "domain_name" {
  default = "matrix.agevega.com"
}

variable "db_host" {}
variable "db_database" {}
variable "db_port" {}
variable "db_user" {}
variable "db_password" {}
variable "secret_key" {}

# RECURSOS
# --------------------------------------

# Configura el proveedor AWS
provider "aws" {
  region = var.aws_region
}

# ------------------------------------------------------------------------------------------------------------------

# Crea un VPC
module "vpc" {
  source = "terraform-aws-modules/vpc/aws"

  name                 = var.vpc_name
  cidr                 = var.vpc_cidr
  azs                  = ["eu-west-1a", "eu-west-1b", "eu-west-1c"]
  public_subnets       = var.public_subnets
  private_subnets      = var.private_subnets
  enable_nat_gateway   = true # La NAT Gateway permite a las instancias en subredes privadas acceder a Internet
  single_nat_gateway   = true # Esta línea indica que se debe utilizar una sola NAT Gateway para todas las zonas de disponibilidad (AZs) en lugar de crear una NAT Gateway por zona de disponibilidad
  enable_vpn_gateway   = false # Un VPN Gateway se utiliza para establecer conexiones de red privada virtual (VPN) entre tu VPC y tu red local o entre dos VPC diferentes
  enable_dns_hostnames = true # Las instancias en el VPC recibirán un nombre de host privado. Esto facilita la conexión y la comunicación entre las instancias en el VPC utilizando nombres de host en lugar de direcciones IP
  tags = {
    Terraform = "true"
    Project   = "Matrix"
  }
}

# Crea un grupo de seguridad
resource "aws_security_group" "matrix_sg" {
  name        = "Matrix"
  description = "Grupo de seguridad de pruebas que permite acceso total de entrada y de salida"
  vpc_id      = module.vpc.vpc_id
}

resource "aws_security_group_rule" "matrix_sg_ingress" {
  security_group_id = aws_security_group.matrix_sg.id

  type        = "ingress"
  from_port   = 0
  to_port     = 0
  protocol    = "tcp"
  cidr_blocks = ["0.0.0.0/0"]
}

resource "aws_security_group_rule" "matrix_sg_egress" {
  security_group_id = aws_security_group.matrix_sg.id

  type        = "egress"
  from_port   = 0
  to_port     = 0
  protocol    = "tcp"
  cidr_blocks = ["0.0.0.0/0"]
}

# Crea una plantilla de lanzamiento
resource "aws_launch_configuration" "matrix_lc" {
  name_prefix     = "Matrix-AmoDeCasa"
  image_id        = var.ami_id
  instance_type   = var.instance_type
  security_groups = [aws_security_group.matrix_sg.id]
  key_name        = var.key_pair

  user_data = <<-EOF
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
DB_HOST=${var.db_host}
DB_DATABASE=${var.db_database}
DB_PORT=${var.db_port}
DB_USER=${var.db_user}
DB_PASSWORD=${var.db_password}
SECRET_KEY=${var.secret_key}
EOT
python3 Aplicacion-Web-CRUD/app.py
EOF

  lifecycle {
    create_before_destroy = true
  }
}


# OUTPUTS
# --------------------------------------

# Muestra la ID del VPC y el nombre como salida
output "vpc_info" {
  value = "VPC Name: ${var.vpc_name}, VPC ID: ${aws_vpc.TEMPLATE_001.id}"
}
