from flask import render_template
from stack import app 
from flask import jsonify
from api import Database

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dialog-team')
def dialog_team():
    return render_template('dialog-team.html')