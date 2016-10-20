import logging
from elasticsearch import Elasticsearch

logger = logging.getLogger('stack')
logger.addHandler(logging.NullHandler())

logger.setLevel(logging.DEBUG)


class Repository(object):

	def __init__(self, config):
		self.es = Elasticsearch([config['elasticsearch']])	
	
	def search_by_query(self, index, query):
		"""
		Sample of query: {"query": {"match_all": {}}}
		see more details on https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl.html
		"""
		resp = self.es.search(index=index, body=query, size=0)
		logger.debug("%d documents found" % resp['hits']['total'])
		
		return resp
		

	def search_technologies(self)

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

		r = Repository({'elasticsearch':'http://104.197.92.45:9200'})
		data = self.es.search(index=index, body=query, size=0)

		for item in data['aggregations']['sheets']['buckets']:
			
			doc_count = item['flow']['buckets'][0]['doc_count']
			print('%s - %s - %s' % (item['key'], item['flow']['buckets'][0]['key'], doc_count))
			
			technologies = item['flow']['buckets'][0]['technologies']['buckets']
			for tech in technologies:
				print ('==> %s' % tech['key'])