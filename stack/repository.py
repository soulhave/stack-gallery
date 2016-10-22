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
	
	def search_by_query(self, index, query):
		"""
		Sample of query: {"query": {"match_all": {}}}
		see more details on https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl.html
		"""
		resp = self.es.search(index=index, body=query, size=0)
		logger.debug("%d documents found" % resp['hits']['total'])
		
		return resp
		

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
		            "technologies": {
		              "terms": {
		                "field": "technology.raw",
		                "size": 36,
		                "order": {
		                  "_count": "desc"
		                }
		              }
		            }
		          }
		        }
		      }
		    }
		  }
		}

		list_tech = []

		index = 'knowledge'		
		data = self.es.search(index=index, body=query, size=0)

		for item in data['aggregations']['sheets']['buckets']:
			
			doc_count = item['flow']['buckets'][0]['doc_count']
			key = item['key']
			flow = item['flow']['buckets'][0]['key']
			
			
			doc = {
				"key": key,
				"flow" : flow,
				"count": doc_count,
				"stack" : []
			}

			print('%s - %s - %s' % (doc['key'], doc['flow'], doc['count']))

			technologies = item['flow']['buckets'][0]['technologies']['buckets']
			for tech in technologies:
				tech_name = tech['key']
				tech_key = re.sub('[^a-zA-Z0-9_]', '_', tech_name.lower())
				image = ( 'https://www.googleapis.com/download/storage/v1/b/tech-gallery-prod/o/%s?&alt=media' % tech_key)
				
				#tc_tech = self.tc.technology(tech_key)
				#if 'image' in tc_tech:
				#	image = tc_tech['image']

				doc_tech = {
					"technology" : tech_key,
					"technologyName": tech_name,
					"imageUrl" : image
				}

				stack = doc['stack']
				stack.append(doc_tech)

				#print ('==> %s - %s' % (tech_name, tech_key))

			list_tech.append(doc)
		return list_tech

#r = Repository({'elasticsearch':'http://104.197.92.45:9200'})				
#techs = r.search_technologies()
#print techs

