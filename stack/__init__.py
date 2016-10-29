from flask import Flask, url_for
import os
import sys

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'SECRET_KEY'


# Function to easily find your assets
# In your template use <link rel=stylesheet href="{{ static('filename') }}">
app.jinja_env.globals['static'] = (
    lambda filename: url_for('static', filename = filename)
)

es_host = os.environ.get('ELASTICSEARCH_URL')
if not es_host:
	sys.exit('Error: You must define ELASTICSEARCH_URL environment variable')


from stack import views
from stack import api