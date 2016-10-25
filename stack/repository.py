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
		

	def search_stack(self):
		index = 'stack'		
		data = self.es.search(index=index, body={"query": {"match_all": {}}}, size=2500, sort='tkci:desc')
		list_stack = []
		for item in data['hits']['hits']:
			list_stack.append(item['_source'])

		return list_stack



	def search_technologies(self):

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

		"""
                  "aggs": {
                    "tkci": {
                        "terms": {
                          "field": "contract.raw",
                          "size": 5,
                          "order": {
                            "_term": "desc"
                            }
                          }
                    }
                  } 
		"""

		projects = []

		index = 'knowledge'		
		data = self.es.search(index=index, body=query, size=0)

		for item in data['aggregations']['sheets']['buckets']:
			
			doc_count = item['flow']['buckets'][0]['doc_count']
			key = item['key']
			flow = item['flow']['buckets'][0]['key']
			tkci = item['flow']['buckets'][0]['tkci']['value']
			
			
			doc = {
				"key": key,
				"flow" : flow,
				"count": doc_count,
				"tkci" : tkci,
				"stack" : []
			}

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
					image = ( 'https://www.googleapis.com/download/storage/v1/b/tech-gallery-prod/o/%s?&alt=media' % tech_key)
					
					## workaround: techgallery image has no pattern for url name
					tc_tech = self.tc.technology(tech_key)
					if 'image' in tc_tech:
						print tc_tech['image']						
						image = tc_tech['image']
					else: 
						image = 'https://techgallery.ciandt.com/assets/images/placeholder.png'

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
