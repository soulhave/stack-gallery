from stack import app 
from flask import jsonify
from elasticsearch import Elasticsearch
from flask import request
from stack import es_host

config = {'elasticsearch':es_host}

@app.route('/stack', methods = ['GET'])
def api_stack():
	r = Database(config)
	stacks = r.list_stack()
	
	return jsonify(stacks)


@app.route('/stack/<id>', methods = ['GET'])
def api_stack_id(id):
	r = Database(config)
	source = request.args.get('_source')
	return jsonify(r.get_stack(id, source))

@app.route('/stack/<id>', methods = ['POST'])
def api_stack_post(id):
	payload = request.json
	print (payload)

	return id, 200


@app.route('/stack/team/<id>', methods = ['GET'])
def api_team(id):
	source='team.*'
	r = Database(config)
	stack = r.get_stack(id, source)

	return jsonify(stack['_source']['team'])



class Database(object):
	def __init__(self, config):
		self.es = Elasticsearch([config['elasticsearch']])	

	def save_document(self, index, document_type, document, id=None):
		res = self.es.index(index=index, doc_type=document_type, body=document, id=id)
		logger.debug("Created documento ID %s" % res['_id'])

	def search_by_query(self, index, query):
		"""
		Sample of query: {"query": {"match_all": {}}}
		"""
		resp = self.es.search(index=index, body=query, size=0)
		logger.debug("%d documents found" % resp['hits']['total'])
		
		return resp

	def list_stack(self):
		index = 'stack'
		data = self.es.search(index=index, body={"query": {"match_all": {}}}, size=2500, sort='name:desc')
		list_stack = []
		for item in data['hits']['hits']:
			stack = item['_source']
			stack['like_count'] = 0
			list_stack.append(item['_source'])

		return list_stack	

	def get_stack(self, id, source):
		if source:
			print source
			return self.es.get(index='stack', doc_type='setting', id=id, _source=source)
		else:
			return self.es.get(index='stack', doc_type='setting', id=id)