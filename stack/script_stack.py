from repository import Repository

r = Repository({'elasticsearch':'http://104.197.92.45:9200'})

projects = r.search_technologies()

for project in projects:
	stack = r.list_stack(project['key'])
	project['stack'] = stack
	r.save_document('stack', 'setting', project, project['key'])
	print ('projet %s created ' % project['key'])
