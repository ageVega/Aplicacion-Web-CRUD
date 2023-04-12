# Configura el proveedor AWS
provider "aws" {
  region = "eu-west-1"
}

# Crea un VPC
resource "aws_vpc" "terraform_test" {
  cidr_block = "10.0.0.0/16"

  tags = {
    Name = "terraform_test"
  }
}

# Muestra la ID del VPC como salida
output "vpc_id" {
  value = aws_vpc.terraform_test.id
}
