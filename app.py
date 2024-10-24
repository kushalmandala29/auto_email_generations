from flask import Flask, request, jsonify, send_from_directory,render_template_string
from flask_cors import CORS
import os
from model.generate import generate
import sys
# print(sys.path)
app = Flask(__name__)
CORS(app)

@app.route('/')
def serve_html():
    return send_from_directory('.', 'template/test3.html')



@app.route('/send_email', methods=['POST'])
def send_email():
    data = request.get_json()
    
    # Extract the data from the request
    to = data.get('to')
    subject = data.get('subject')
    message = data.get('message')
    
 
    # Simulate a successful email sending response
    response = {
        "status": "success",
        "message": "Email sent successfully!",
        "data": {
            "to": to,
            "subject": subject,
            "message": generate(message)
        }
    }





    
    return jsonify(response), 200




if __name__ == '__main__':
    app.run(host='localhost', port=8000,debug=True)