import os
import logging
import re
from elasticsearch import Elasticsearch
import json

from techgallery import TechGallery
import config


logger = logging.getLogger('stack')
logger.addHandler(logging.NullHandler())

logger.setLevel(logging.DEBUG)


class Stack(object):

	def __init__(self):
		self.config = config.load()
		self.es = Elasticsearch([self.config['repository']['elasticsearch']['host']])	
		self.tc = TechGallery(self.config['techgallery'])


	def load_stack(self, project):
		"""
			project must have a structure like this:
				doc = {
					"key": - id
					"owner" : 
					"name" : 
					"index" : 
				}

		"""

		self.createTemplateIfNotExits('stack')

		key = project['key']
		# add technologies list
		techs = self.list_stack(key)
		project['stack_size'] = len(techs) if techs else 0
		project['stack'] = techs
		# add team members
		team = self.list_team(key)
		project['team_size'] = len(team) if team else 0
		project['team'] = team
		## save document
		self.save_document('stack', 'setting', project, key)


	def createTemplateIfNotExits(self, index):
		"""if template doesn't exists, create one from json file definition 
		Method reads a template definition from file on path ./resources ('%s-template.json' % index)
		where index is a method's parameter
		"""
		if not self.es.indices.exists_template(name=index):
			resource_path = os.path.join(os.path.split(__file__)[0], ("resources/%s-template.json" % index ))
			with open(resource_path) as data_file:    
			    settings = json.load(data_file)
			
			# create index
			#response = self.es.indices.create(index=index, ignore=400, body=settings)
			response = self.es.indices.put_template(name=index, body=settings)
			logger.debug("Template %s created"  % response['acknowledged'])
	
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

		black_list = {'backbone.js':'backbone.js', 
			'calabash':'cabalash', 
			'node.js':'node.js', 
			'asp.net core':'asp.net_core', 
			'asp.net webforms': 'asp.net_webforms',
			'asp.net webapi': 'asp.net_webapi',
			'asp.net mvc': 'asp.net_mvc',
			'quartz.net': 'quartz.net'
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
					if tech_name:
						if tech_name.lower() in black_list:
							tech_key = black_list[tech_name.lower()]
						else:
							tech_key = re.sub('[#/ ]', '_', re.sub('[^\x00-\x7F]', '_', re.sub('[.]', '', tech_name.lower())))
						image = 'https://techgallery.ciandt.com/assets/images/placeholder.png'
						
						## workaround: techgallery image has no pattern for url name
						(tc_tech, status_code) = self.tc.technology(tech_key)
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
						"email": '%s@ciandt.com'%login,
						"image": "https://citweb.cit.com.br/ipeople/photo?cdLogin=%s"%login
					}

					team.append(doc)

		return team	

	def save_document(self, index, doc_type, document, id=None):
		res = self.es.index(index=index, doc_type=doc_type, body=document, id=id)
		logger.debug("Created documento ID %s" % res['_id'])


	def exists(self, index, doc_type, id):
		return self.es.exists(index=index, doc_type=doc_type, id=id)

