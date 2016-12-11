"""Main View. Handle users interactions."""
from server import app, client_path
from flask import send_file
from datetime import datetime
import os


@app.after_request
def after_request(response):
    """Add headers for every response with no-cache control."""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "-1"
    response.headers['Last-Modified'] = datetime.now()

    return response


@app.route('/')
def index():
    """Main endpoint sends response with index.html file."""
    return send_file(os.path.join(client_path, 'index.html'))
