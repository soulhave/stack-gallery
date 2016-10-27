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
				"contract" : contract['key'],
				"flow" : flow['key'],
				"count": doc_count,
				"tkci" : tkci,
				"stack" : []
			}

			#print doc

			#print('%s - %s - %s' % (doc['key'], doc['flow'], tkci))
			projects.append(doc)
		return projects


	def list_projects(self, sheet_id):

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
