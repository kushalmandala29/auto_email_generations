# output "ec2_public_ip" {
#   value = aws_instance.my_app_ec2.public_ip
# }

# output "ecr_repository_url" {
#   value = aws_ecr_repository.my_app_repo.repository_url
# }


output "ecr_repository_url" {
  description = "The URL of the ECR repository"
  value       = aws_ecr_repository.my_ecr_repo.repository_url
}

output "ec2_public_ip" {
  description = "The public IP address of the EC2 instance"
  value       = aws_instance.web.public_ip
}
