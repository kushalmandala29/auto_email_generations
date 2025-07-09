# 📨 Auto Email Generations

A Python-based tool to automatically generate personalized email drafts using predefined templates and dynamic input parameters. Ideal for streamlining communication in a professional or business environment.

## 🚀 Features

- Uses Jinja2 templating for flexible email formats.
- Accepts dynamic input like recipient name, tone, and context.
- Optional AI-based text generation or enhancement.
- Simple CLI interface for generating emails.
- Easily customizable templates and parameters.

## 📁 Project Structure

auto_email_generations/
├── app.py # Main CLI application
├── requirements.txt # Python dependencies
├── template/ # Email templates (Jinja2 format)
│ └── example_template.j2
├── model/ # AI/ML model logic (optional)
├── terraform/ # Infrastructure as code (if used)
├── workflows/ # GitHub Actions workflows
└── README.md # Project documentation



## ⚙️ Installation

Clone the repo and install dependencies:

```bash
git clone https://github.com/kushalmandala29/auto_email_generations.git
cd auto_email_generations
pip install -r requirements.txt


python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`


python app.py \
  --template template/example_template.j2 \
  --to "john@example.com" \
  --subject "Welcome!" \
  --params name=John company=OpenAI tone=friendly
