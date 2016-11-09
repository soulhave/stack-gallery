from stack import app 
from stack.security import login_required, parser_webtoken_token

from flask import render_template
from datetime import datetime

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "-1"
    response.headers['Last-Modified'] = datetime.now()
    
    # oauth_token = parser_webtoken_token()
    # if oauth_token: 
    #     response.headers['Authorization'] = oauth_token

    return response

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/stacks')
def stacks():
    return render_template('stacks.html')


@app.route('/dialog-team')
def dialog_team():
    return render_template('dialog-team.html')