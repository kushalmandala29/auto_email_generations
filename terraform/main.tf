

# Create an ECR Repository
resource "aws_ecr_repository" "my_app" {
  name                 = "my-app-repo"
  image_tag_mutability = "MUTABLE"
  image_scanning_configuration {
    scan_on_push = true
  }
}

# Create a Security Group for EC2 instance
resource "aws_security_group" "ec2_sg" {
  name        = "ec2-security-group"
  description = "Allow SSH and HTTP access"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]  # Allow SSH access from anywhere (you can restrict this)
  }

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]  # Allow HTTP access
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]  # Allow all outbound traffic
  }
}

# Create an EC2 Instance with Docker installed via user_data
resource "aws_instance" "my_ec2" {
  ami           = "ami-0c55b159cbfafe1f0"  # Example Amazon Linux 2 AMI, replace with your own if needed
  instance_type = "t2.micro"
  key_name      = "your-ec2-key"  # Replace with your EC2 key pair name
  security_groups = [aws_security_group.ec2_sg.name]

  # Install Docker using the user data script
  user_data = <<-EOF
              #!/bin/bash
              sudo yum update -y
              sudo amazon-linux-extras install docker -y
              sudo service docker start
              sudo usermod -aG docker ec2-user
              sudo chkconfig docker on
              EOF

  tags = {
    Name = "MyAppEC2Instance"
  }
}

output "ecr_repository_url" {
  value = aws_ecr_repository.my_app.repository_url
}

output "ec2_public_ip" {
  value = aws_instance.my_ec2.public_ip
}
