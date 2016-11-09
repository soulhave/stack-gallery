from stack.util import get_environ

from flask import Flask, url_for
import sys
import logging

mode = sys.argv[1] if len(sys.argv) > 1 else 'development'

app = Flask('stack')

################
#### config ####
################
app.config.from_json('%s.json' % mode)

# Function to easily find your assets
# In your template use <link rel=stylesheet href="{{ static('filename') }}">
app.jinja_env.globals['static'] = (
    lambda filename: url_for('static', filename = filename)
)

app.config['GOOGLE_CLIENT_SECRET'] = get_environ(app.config, 'GOOGLE_CLIENT_SECRET')
app.config['GOOGLE_CLIENT_ID'] = get_environ(app.config, 'GOOGLE_CLIENT_ID')
app.config['ELASTICSEARCH_URL'] = get_environ(app.config, 'ELASTICSEARCH_URL')

########################
#### logging config ####
########################
if (2, 7) <= sys.version_info < (3, 2):
	# On Python 2.7 and Python3 < 3.2, install no-op handler to silence
	# `No handlers could be found for logger "elasticsearch"` message per
	# <https://docs.python.org/2/howto/logging.html#configuring-logging-for-a-library>
	FORMAT = '%(name)s %(levelname)-5s %(message)s'
	logging.basicConfig(format=FORMAT)
	for item in app.config['LOGGER']:
		logging.getLogger(item['NAME']).setLevel(int(item['LEVELNO']))

logger = logging.getLogger('stack')
logger.info('starting app => %s ' % id(app))
logger.info('starting mode => %s ' % mode)

##############
#### view ####
##############
from stack import view_stack
from stack import view_auth

##############
#### APIs ####
##############
from stack import api_stacks
from stack import api_users
from stack import api_technologies
from stack import api_trends
from stack import api_auth