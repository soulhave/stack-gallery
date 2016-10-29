import logging
import re
from elasticsearch import Elasticsearch
from techgallery import TechGallery

logger = logging.getLogger('stack')
logger.addHandler(logging.NullHandler())

logger.setLevel(logging.DEBUG)


class Repository(object):

	def __init__(self, config):
		self.es = Elasticsearch([config['elasticsearch']])	
		self.tc = TechGallery({'endpoint':'https://tech-gallery.appspot.com/_ah/api/rest/v1'})
	
	def list_projects(self):

		query = {
		  "size": 0,
		  "query": {
		    "query_string": {
		      "query": "*",
		      "analyze_wildcard": "true"
		    }
		  },
		  "aggs": {
		    "sheets": {
		      "terms": {
		        "field": "sheet_id.raw",
		        "size": 0,
		        "order": {
		          "_count": "desc"
		        }
		      },
		      "aggs": {
		        "contract": {
		          "terms": {
		            "field": "contract.raw",
		            "order": {
		              "_count": "desc"
		            }
		          },
			      "aggs": {
			        "flow": {
			          "terms": {
			            "field": "flow.raw",
			            "order": {
			              "_count": "desc"
			            }
			          },
		              "aggs": {
		                "tkci": {
		                  "sum": {
		                    "field": "skill_index"
		                  }
		                }
		              }                       
			        }
			      }                  
		        }
		      }
		    }
		  }
		}


		projects = []

		index = 'knowledge'		
		data = self.es.search(index=index, body=query, size=0)

		for item in data['aggregations']['sheets']['buckets']:
			
			doc_count = item['doc_count']
			key = item['key']
			contract = item['contract']['buckets'][0]
			flow = contract['flow']['buckets'][0]
			tkci = flow['tkci']['value']
						
			doc = {
				"key": key,
				"owner" : contract['key'],
				"name" : flow['key'],
				"index" : tkci
			}

			#print doc

			#print('%s - %s - %s' % (doc['key'], doc['flow'], tkci))
			projects.append(doc)
		return projects


	def list_stack(self, sheet_id):

		query = {
		    "query": {"match": {
		       "sheet_id": sheet_id
		    }}
		}

		stack = []

		index = 'project'		
		data = self.es.search(index=index, body=query, size=1)

		for project in data['hits']['hits']:
			item = project['_source']
			#print item['stack']

			if 'stack' in item:
				for tech in item['stack']:
					tech_name = tech
					tech_key = re.sub('[#/ ]', '_', re.sub('[^\x00-\x7F]', '_', re.sub('[.]', '', tech_name.lower())))
					image = 'https://techgallery.ciandt.com/assets/images/placeholder.png'
					
					## workaround: techgallery image has no pattern for url name
					tc_tech = self.tc.technology(tech_key)
					if 'image' in tc_tech:
						logger.debug(tc_tech['image'])
						image = tc_tech['image']

					doc_tech = {
						"technology" : tech_key,
						"technologyName": tech_name,
						"imageUrl" : image
					}
					# add new tech definition
					stack.append(doc_tech)
			else: 
				print 'ERROR =>  project with no stack'
			return stack

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

			logger.debug(item)

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

	def save_document(self, index, doc_type, document, id=None):
		res = self.es.index(index=index, doc_type=doc_type, body=document, id=id)
		logger.info("Created documento ID %s" % res['_id'])


	def exists(self, index, doc_type, id):
		return self.es.exists(index=index, doc_type=doc_type, id=id)

