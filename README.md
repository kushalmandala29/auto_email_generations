# 🤖 Auto Email Generation System

This project is an **AI-powered automated email generation system** that leverages large language models (LLMs) to dynamically generate context-aware emails. It is designed to run efficiently on **AWS EC2** using **Ollama LLM**, with a production-grade setup using **CI/CD pipelines** and **Terraform** for infrastructure automation.

---

## 🚀 Features

- ✉️ **AI-based Email Generation** using the lightweight and local Ollama model
- ☁️ **AWS EC2 Deployment** with optimized configuration
- 🔄 **CI/CD Pipeline Integration** for automated testing and deployment
- 🛠️ **Infrastructure as Code (IaC)** with **Terraform** for consistent and reproducible environments
- 🧩 Modular and scalable code structure
- 📦 Dockerized setup for easy portability

---

## 🧱 Architecture

```plaintext
+-------------+        +-----------+       +------------------+
|  Frontend   | <----> |  Backend  | <---> |  Ollama LLM API  |
+-------------+        +-----------+       +------------------+
      |                    |
      |                    V
      |               AWS EC2 Instance
      |
      V
CI/CD (GitHub Actions / Any Tool)
      |
      V
Infrastructure via Terraform
```
## Technologies Used
- Ollama – Lightweight LLM for local inference

- Python / Flask / FastAPI – Backend logic

- Terraform – Infrastructure provisioning

- AWS EC2 – Hosting environment

- GitHub Actions – CI/CD pipeline

- Docker – Containerization


## 🚀 Quick Start (Using Bash Scripts)

### 1. Clone the Repository

```bash
git clone https://github.com/kushalmandala29/auto_email_generations.git
cd auto_email_generations
```
### 2. Provision Infrastructure with Terraform
``` bash
cd terraform
terraform init
terraform apply
```

### 3. SSH into the EC2 Instance
```bash
ssh -i path/to/key.pem ec2-user@<EC2_PUBLIC_IP>
```
### 4. Run the Setup Script
```bash
cd auto_email_generations/scripts
bash setup.sh
```

### 5. Start the Server
```bash
bash start_server.sh
```

## 📦 Environment Variables
### Create a .env file in the root (if needed):
```bash
PORT=5000
MODEL_NAME=llama2
EMAIL_TEMPLATE_VERSION=v1
```

### 💻 Sample Script Usage
```bash
# One-liner full setup & start (after Terraform):
ssh -i key.pem ec2-user@<EC2_IP> "bash -s" < scripts/setup.sh && scripts/start_server.sh
```

## 🔒 Security Notes
## Ensure your .pem file is secure

## Do not expose ports publicly unless behind a firewall or auth layer

## Ollama model should be verified before deployment


