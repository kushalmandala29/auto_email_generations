from flask import Flask, render_template, request, jsonify
# from template import *

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('template/email.html')



if __name__ == '__main__':
    app.run(host='localhost', port=8080,debug=True)