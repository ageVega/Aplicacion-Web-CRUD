
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
  default = [
    "10.0.0.0/20",
    "10.0.16.0/20",
    "10.0.32.0/20"
  ]
}

variable "private_subnets" {
  default = [
    "10.0.128.0/20",
    "10.0.144.0/20",
    "10.0.160.0/20"
  ]
}


variable "ami_id" {
  default = "ami-06d94a781b544c133" # Ubuntu Server 22.04 LTS, actualiza este valor si es necesario
}

variable "instance_type" {
  default = "t2.micro"
}

variable "key_pair" {
  default = "miami"
}

variable "domain_name" {
  default = "matrix.agevega.com"
}

variable "db_host" {}
variable "db_database" {}
variable "db_port" {}
variable "db_user" {}

variable "db_password" {
  sensitive = true # Evita que el valor de la variable aparezca en la salida de la línea de comandos de Terraform
}

variable "secret_key" {
  sensitive = true # Evita que el valor de la variable aparezca en la salida de la línea de comandos de Terraform
}

variable "certificate_arn" {
  description = "The ARN of the SSL certificate for the HTTPS listener"
  type        = string
}

variable "certificate_arn_amodecasa" {
  description = "The ARN of the SSL certificate for the HTTPS listener for amodecasa.agevega.com"
  type        = string
}

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
  enable_dns_support   = true # Asegura que las instancias en el VPC reciban un nombre de host público
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

/*
resource "aws_security_group_rule" "matrix_sg_ingress_all" {
  security_group_id = aws_security_group.matrix_sg.id

  type        = "ingress"
  from_port   = 0
  to_port     = 65535
  protocol    = "tcp"
  cidr_blocks = ["0.0.0.0/0"]
}

resource "aws_security_group_rule" "matrix_sg_ingress_ssh" {
  security_group_id = aws_security_group.matrix_sg.id

  type        = "ingress"
  from_port   = 22
  to_port     = 22
  protocol    = "tcp"
  cidr_blocks = ["0.0.0.0/0"]
}
*/

resource "aws_security_group_rule" "matrix_sg_ingress_http" {
  security_group_id = aws_security_group.matrix_sg.id

  type        = "ingress"
  from_port   = 80
  to_port     = 80
  protocol    = "tcp"
  cidr_blocks = ["0.0.0.0/0"]
}

resource "aws_security_group_rule" "matrix_sg_ingress_https" {
  security_group_id = aws_security_group.matrix_sg.id

  type        = "ingress"
  from_port   = 443
  to_port     = 443
  protocol    = "tcp"
  cidr_blocks = ["0.0.0.0/0"]
}

resource "aws_security_group_rule" "matrix_sg_ingress_app" {
  security_group_id = aws_security_group.matrix_sg.id

  type        = "ingress"
  from_port   = 8080
  to_port     = 8080
  protocol    = "tcp"
  cidr_blocks = ["0.0.0.0/0"]
}

resource "aws_security_group_rule" "matrix_sg_egress" {
  security_group_id = aws_security_group.matrix_sg.id

  type        = "egress"
  from_port   = 0
  to_port     = 0
  protocol    = "-1"
  cidr_blocks = ["0.0.0.0/0"]
}

# Crea una plantilla de lanzamiento
resource "aws_launch_template" "matrix_lt" {
  name_prefix   = "Matrix-AmoDeCasa"
  image_id      = var.ami_id
  instance_type = var.instance_type
  key_name      = var.key_pair

  network_interfaces {
    associate_public_ip_address = true
    security_groups             = [aws_security_group.matrix_sg.id]
  }

  user_data = base64encode(<<-EOF
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
  )

  lifecycle {
    create_before_destroy = true
  }
}

# Crea un Target Group
resource "aws_lb_target_group" "matrix_tg" {
  name     = "Matrix-AmoDeCasa"
  port     = 8080
  protocol = "HTTP"
  vpc_id   = module.vpc.vpc_id

  health_check {
    protocol = "HTTP"
    path     = "/auth/login"
    port     = "8080"
  }
}

# Crea un Application Load Balancer
resource "aws_lb" "matrix_alb" {
  name               = "Matrix-AmoDeCasa"
  internal           = false # Crea un balanceador de carga público accesible desde Internet
  load_balancer_type = "application"
  security_groups    = [aws_security_group.matrix_sg.id]
  subnets            = module.vpc.public_subnets

  tags = {
    Name = "Matrix-AmoDeCasa"
  }
}

# Crea un Listener para el puerto 80
resource "aws_lb_listener" "matrix_http" {
  load_balancer_arn = aws_lb.matrix_alb.arn
  port              = 80
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.matrix_tg.arn
  }
}

# Crea un Listener para el puerto 443
resource "aws_lb_listener" "matrix_https" {
  load_balancer_arn = aws_lb.matrix_alb.arn
  port              = 443
  protocol          = "HTTPS"
  ssl_policy        = "ELBSecurityPolicy-2016-08"
  certificate_arn   = var.certificate_arn

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.matrix_tg.arn
  }
}

# Crea un Listener para el puerto 443 para amodecasa.agevega.com
resource "aws_lb_listener" "amodecasa_https" {
  load_balancer_arn = aws_lb.matrix_alb.arn
  port              = 443
  protocol          = "HTTPS"
  ssl_policy        = "ELBSecurityPolicy-2016-08"
  certificate_arn   = var.certificate_arn_amodecasa

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.matrix_tg.arn
  }
}

# Crea un grupo de autoescalado
resource "aws_autoscaling_group" "matrix_asg" {
  name_prefix          = "Matrix-AmoDeCasa"
  launch_template {
    id      = aws_launch_template.matrix_lt.id
    version = "$Latest"
  }
  vpc_zone_identifier  = module.vpc.public_subnets

  min_size = 1
  max_size = 1
  desired_capacity = 1

  target_group_arns = [aws_lb_target_group.matrix_tg.arn]

  health_check_type         = "ELB"
  health_check_grace_period = 300 # 5 minutos

  lifecycle {
    create_before_destroy = true
  }
}



# OUTPUTS
# --------------------------------------

# Muestra la ID del VPC y el nombre como salida
output "vpc_info" {
  value = "VPC Name: ${var.vpc_name}, VPC ID: ${module.vpc.vpc_id}"
}

output "public_subnets_ids" {
  description = "The IDs of the public subnets"
  value       = module.vpc.public_subnets
}

output "private_subnets_ids" {
  description = "The IDs of the private subnets"
  value       = module.vpc.private_subnets
}

# Muestra la ID del grupo de seguridad y el nombre como salida
output "sg_info" {
  value = "SG Name: ${aws_security_group.matrix_sg.name}, SG ID: ${aws_security_group.matrix_sg.id}"
}

# Muestra la ID del grupo de autoescalado y el nombre como salida
output "asg_info" {
  value = "ASG Name: ${aws_autoscaling_group.matrix_asg.name}, ASG ID: ${aws_autoscaling_group.matrix_asg.id}"
}

# Muestra la ID de la plantilla de lanzamiento y el nombre como salida
output "lt_info" {
  value = "LT Name: ${aws_launch_template.matrix_lt.name}, LT ID: ${aws_launch_template.matrix_lt.id}"
}

# Muestra la ID del grupo de balanceo de carga y el nombre como salida
output "tg_info" {
  value = "TG Name: ${aws_lb_target_group.matrix_tg.name}, TG ID: ${aws_lb_target_group.matrix_tg.id}"
}

# Muestra la ID del grupo de balanceo de carga y el nombre como salida
output "alb_info" {
  value = "ALB Name: ${aws_lb.matrix_alb.name}, ALB ID: ${aws_lb.matrix_alb.id}"
}

output "listener_80_info" {
  description = "Information about the Listener for port 80"
  value       = "Listener ARN: ${aws_lb_listener.matrix_http.arn}"
}

output "listener_443_info" {
  description = "Information about the Listener for port 443"
  value       = "Listener ARN: ${aws_lb_listener.matrix_https.arn}"
}

output "listener_443_amodecasa_info" {
  description = "Information about the Listener for port 443 for amodecasa.agevega.com"
  value       = "Listener ARN: ${aws_lb_listener.amodecasa_https.arn}"
}

output "alb_dns_name" {
  value = aws_lb.matrix_alb.dns_name
}
