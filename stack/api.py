from stack import app 
from flask import jsonify
from elasticsearch import Elasticsearch

@app.route('/stack', methods = ['GET'])
def api_stack():
	r = Database({'elasticsearch':'http://104.197.92.45:9200'})
	techs = r.list_stack()
	
	return jsonify(techs)

@app.route('/team/<sheet_id>', methods = ['GET'])
def api_team(sheet_id):
	r = Database({'elasticsearch':'http://104.197.92.45:9200'})
	team = r.list_team(sheet_id)
	
	return jsonify(team)

class Database(object):
	def __init__(self, config):
		self.es = Elasticsearch([config['elasticsearch']])	

	def save_document(self, index, document_type, document, id=None):
		res = self.es.index(index=index, doc_type=document_type, body=document, id=id)
		logger.debug("Created documento ID %s" % res['_id'])

	def search_by_query(self, index, query):
		"""
		Sample of query: {"query": {"match_all": {}}}
		see more details on https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl.html
		"""
		resp = self.es.search(index=index, body=query, size=0)
		logger.debug("%d documents found" % resp['hits']['total'])
		
		return resp

	def list_stack(self):
		index = 'stack'		
		data = self.es.search(index=index, body={"query": {"match_all": {}}}, size=2500, sort='tkci:desc')
		list_stack = []
		for item in data['hits']['hits']:
			stack = item['_source']
			stack['like_count'] = 0
			list_stack.append(item['_source'])

		return list_stack		

	def list_team(self, sheet_id):

		query = {
		    "query": {"match": {
		       "sheet_id": sheet_id
		    }}
		}

		team = []

		index = 'project'		
		data = self.es.search(index=index, body=query, size=1)

		for project in data['hits']['hits']:
			item = project['_source']

			print (item)

			if 'team' in item:
				for login in item['team']:
					doc = {
						"login" : login,
						"name": 'nome completo',
						"email": '%s@ciandt.com'%login,
						"image": "https://citweb.cit.com.br/ipeople/photo?cdLogin=%s"%login
					}

					team.append(doc)

		return team		