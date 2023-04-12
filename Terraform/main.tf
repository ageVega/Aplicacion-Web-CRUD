# Configura el proveedor AWS
provider "aws" {
  region = "eu-west-1"
}

# Define la variable global
variable "vpc_name" {
  default = "TEMPLATE_001"
}

# Crea un VPC
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
