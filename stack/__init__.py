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

if (2, 7) <= sys.version_info < (3, 2):
	# On Python 2.7 and Python3 < 3.2, install no-op handler to silence
	# `No handlers could be found for logger "elasticsearch"` message per
	# <https://docs.python.org/2/howto/logging.html#configuring-logging-for-a-library>
	import logging
	FORMAT = '%(name)s %(levelname)-5s %(message)s'
	logging.basicConfig(format=FORMAT)
	logger = logging.getLogger('stack')
	logger.addHandler(logging.NullHandler())
	logger.setLevel(logging.DEBUG)

	logging.getLogger('elasticsearch').setLevel(logging.INFO)
	logging.getLogger('elasticsearch.trace').setLevel(logging.INFO)

es_host = os.environ.get('ELASTICSEARCH_URL')
if not es_host:
	sys.exit('Error: You must define ELASTICSEARCH_URL environment variable')

from stack import view_stack
from stack import view_auth
from stack import api_stacks
from stack import api_users
from stack import api_technologies