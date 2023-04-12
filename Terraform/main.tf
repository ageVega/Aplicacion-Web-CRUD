# Configura el proveedor AWS
provider "aws" {
  region     = "us-west-2"
  access_key = "<tu_access_key>"
  secret_key = "<tu_secret_key>"
}

# Crea un VPC
resource "aws_vpc" "mi_vpc" {
  cidr_block = "10.0.0.0/16"

  tags = {
    Name = "mi-vpc"
  }
}

# Muestra la ID del VPC como salida
output "vpc_id" {
  value = aws_vpc.mi_vpc.id
}
