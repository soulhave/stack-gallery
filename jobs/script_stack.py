import os
import sys
import logging
from stack import Stack

# logging definitions
FORMAT = '%(name)s %(levelname)-5s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger('stack')
logger.addHandler(logging.NullHandler())
logger.setLevel(logging.DEBUG)
logging.getLogger('elasticsearch').setLevel(logging.ERROR)

stack = Stack()

option = sys.argv[1] if len(sys.argv) > 1 else 'nome'
if option.lower() == 'full':
	projects = stack.list_projects()
else:
	projects = [item for item in stack.list_projects() if not stack.exists('stack', 'setting', item['key'])]
logger.info('%s projects ' % len(projects))

stack.createTemplateIfNotExits('stack')

for project in projects:
	key = project['key']
	# add technologies list
	logger.info('starting %s' % key)
	stack.load_stack(project)