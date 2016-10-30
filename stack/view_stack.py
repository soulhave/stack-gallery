from stack import app 
from security import login_required

from flask import render_template

@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/dialog-team')
def dialog_team():
    return render_template('dialog-team.html')