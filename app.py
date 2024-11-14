from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
# from model.generate import ModelConfig, EmailContent, EmailGenerator, EmailParser
from model.pipe_line import EmailGenerationPipeline
from model.generate import DataStructurer, StructuringCallbackHandler 

app = Flask(__name__)
CORS(app)

@app.route('/')
def serve_html():
    return send_from_directory('.', 'template/original.html')

@app.route('/generate_email_content', methods=['POST'])
def generate_email_content():
    data = request.get_json()
    # subject = data.get('subject')
    body = data.get('body')
    To = data.get('To')
    
    # Define the recipient's email address (hardcoded)
    # recipient_email = "example@recipient.com"
    
    # Generate email content based on subject and body input
    pipeline = EmailGenerationPipeline()
    generated_output = pipeline.process(body)  # Update to pass subject and body
    
    # Add the "To" recipient to the email content
    full_email_content = f"To: {To}\n{generated_output}"

    return jsonify({"email_body": full_email_content}), 200

if __name__ == '__main__':
    app.run(host='localhost', port=8000, debug=True)