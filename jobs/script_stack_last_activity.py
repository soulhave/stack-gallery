import os
import sys
import logging
from stack import Stack
from client import TechAnalytics

# logging definitions
FORMAT = '%(name)s %(levelname)-5s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger('stack')
logger.addHandler(logging.NullHandler())
logger.setLevel(logging.INFO)
logging.getLogger('elasticsearch').setLevel(logging.ERROR)
logging.getLogger('googleapiclient.http').setLevel(logging.ERROR)
logging.getLogger('googleapiclient.discovery_cache').setLevel(logging.ERROR)

stack = Stack()
ta = TechAnalytics()
repository = ta.get_repository()

# get spreadsheets updated from 10 minutos ago to now
query = {"query": {"range": {"@timestamp": {"gte" : "now-10m","lt" :  "now"}}}}

spreadsheets = repository.searchByQuery('archboard', query)
logger.info('total %s sheets' % spreadsheets['hits']['total'])

for spreadsheet in spreadsheets['hits']['hits']:
	logger.info('starting %s' % spreadsheet['_source']['sheet_id'])	
	logger.info('=> loading sheet knowledge_map')
	project = ta.load_sheet_knowledge_map(spreadsheet)

	logger.info('=> loading stack')
	stack.load_stack(project)

logger.info('spreadsheet process finished')


