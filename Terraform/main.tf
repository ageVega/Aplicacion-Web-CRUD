
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
    "eu-west-1a" = "10.0.1.0/24"
    "eu-west-1b" = "10.0.2.0/24"
    "eu-west-1c" = "10.0.3.0/24"
  }
}

variable "private_subnets" {
  default = {
    "eu-west-1a" = "10.0.101.0/24"
    "eu-west-1b" = "10.0.102.0/24"
    "eu-west-1c" = "10.0.103.0/24"
  }
}

variable "ami_id" {
  default = "ami-0c94855ba95b798c7" # Ubuntu Server 22.04 LTS, actualiza este valor si es necesario
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

# RECURSOS
# --------------------------------------

# Configura el proveedor AWS
provider "aws" {
  region = var.aws_region
}

# Crea una VPC
resource "aws_vpc" "TEMPLATE_001" {
  cidr_block = "10.0.0.0/16"

  tags = {
    Name = var.vpc_name
  }
}

# Muestra la ID del VPC y el nombre como salida
output "vpc_info" {
  value = "VPC Name: ${var.vpc_name}, VPC ID: ${aws_vpc.TEMPLATE_001.id}"
}
