import os
import sys
import logging
from elasticsearch import Elasticsearch
import json

es_host = os.environ.get('ELASTICSEARCH_URL_SOURCE')
es_target = os.environ.get('ELASTICSEARCH_URL_SOURCE')
if not es_host:
	sys.exit('Error: You must define ELASTICSEARCH_URL environment variable')

es_source = Elasticsearch([es_host])
index = 'stack'
query = '{"query": {"match_all": {}}}'
data = es_source.search(index=index, body=query, size=2500)

# with open('result.json', 'w') as fp:
# 	json.dump(data['hits']['hits'], fp)

es_target = Elasticsearch([es_target], http_auth=(user, password))

for item in data['hits']['hits']:
	es_target.index(index=index, doc_type='setting', id=item['_id'], body=item['_source'])
