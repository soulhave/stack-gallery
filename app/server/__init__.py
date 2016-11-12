from server import util

from flask import Flask
import sys
import logging
import os

mode = sys.argv[1] if len(sys.argv) > 1 else 'development'

current_path = os.path.dirname(__file__)
client_path = os.path.abspath(os.path.join(current_path, '..', 'client'))

app = Flask('stack', static_url_path='', static_folder=client_path)

################
#### config ####
################
app.config.from_json('%s.json' % mode)
app.config['GOOGLE_CLIENT_SECRET'] = util.get_environ(app.config, 'GOOGLE_CLIENT_SECRET')
app.config['GOOGLE_CLIENT_ID'] = util.get_environ(app.config, 'GOOGLE_CLIENT_ID')
app.config['ELASTICSEARCH_URL'] = util.get_environ(app.config, 'ELASTICSEARCH_URL')

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

# ##############
# #### APIs ####
# ##############
import view
import api