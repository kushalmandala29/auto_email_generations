variable "region" {
  description = "AWS region"
  default     = "us-east-1"
}

variable "instance_type" {
  description = "Type of EC2 instance"
  default     = "t2.micro"
}

variable "key_name" {
  description = "Name of the SSH key pair"
}

variable "ecr_repository_name" {
  description = "ECR repository name"
  default     = "your-ecr-repo"
}

variable "vpc_id" {
  description = "VPC ID for EC2 instance"
}
