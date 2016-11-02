import os
import sys
import logging
from repository import Repository

# logging definitions
FORMAT = '%(name)s %(levelname)-5s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger('stack')
logger.addHandler(logging.NullHandler())
logger.setLevel(logging.DEBUG)
logging.getLogger('elasticsearch').setLevel(logging.ERROR)

es_host = os.environ.get('ELASTICSEARCH_URL')
if not es_host:
	sys.exit('Error: You must define ELASTICSEARCH_URL environment variable')
r = Repository({'elasticsearch': es_host})

option = sys.argv[1] if len(sys.argv) > 1 else 'nome'

if option.lower() == 'full':
	projects = r.list_projects()
else:
	projects = [item for item in r.list_projects() if not r.exists('stack', 'setting', item['key'])]
logger.info('%s projects ' % len(projects))

r.createTemplateIfNotExits('stack')

for project in projects:
	key = project['key']
	# add technologies list
	logger.info('starting %s' % key)
	techs = r.list_stack(key)
	project['stack_size'] = len(techs) if techs else 0
	project['stack'] = techs
	# add team members
	team = r.list_team(key)
	project['team_size'] = len(team) if team else 0
	project['team'] = team
	## save document
	r.save_document('stack', 'setting', project, key)
	print ('projet %s created ' % key)
