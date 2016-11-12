from server import app, client_path

from flask import send_file
from datetime import datetime
import os

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "-1"
    response.headers['Last-Modified'] = datetime.now()
    
    return response

@app.route('/')
def index():
    return send_file(os.path.join(client_path, 'index.html'))