# Configura el proveedor AWS
provider "aws" {
  region     = "eu-west-1"
}

# Crea un VPC
resource "aws_vpc" "mi_vpc_test" {
  cidr_block = "10.0.0.0/16"

  tags = {
    Name = "mi-vpc"
  }
}

# Muestra la ID del VPC como salida
output "vpc_id" {
  value = aws_vpc.mi_vpc_test.id
}
