import logging
import os
import json
import config
from people import People
from techgallery import TechGallery
from knowledgemap import KnowledgeMap
from elasticsearch import Elasticsearch
from apiclient import errors
import send_gmail

logger = logging.getLogger('stack')

class TechAnalytics(object):

	def __init__(self):
		self.config = config.load()
		self.people = People(self.config['people'])
		self.techgallery = TechGallery(self.config['techgallery'])
		self.repository = Repository(self.config['repository'])	
		self.knowledge = KnowledgeMap(self.config['knowledgemap'])	

	def get_repository(self):
		return self.repository

	def load_people(self):
		p = self.people
		repository = self.repository

		count = 0

		for hit in p.loadAll():
			count += 1
			logger.info("Loading %s - %s  " % (hit['login'], count))
			project = p.loadProjectFromHtml(hit['login'])

			#birthday = 341193600000
			#date = datetime.utcfromtimestamp(birthday / 1000)
			#print date

			doc = {
		       'name' : hit['name'],
		       'login': hit['login'],
		       'role' : hit['role'],
		       'cityBase' : hit['cityBase'],
		       'project': {
		       		'code' : hit['project']['code'],
		       		'name' : project
		       },
		       'area' : hit['area'],
		       'company' : hit['company']
				}
			
			## create index doc
			repository.createTemplateIfNotExits('people')
			repository.saveDocument('people', 'login', doc, hit['login'])


	def load_skill(self):
		repository = self.repository
		tc = self.techgallery

		## retrieve all people
		query = {"query": {"match_all": {}}}
		data = repository.searchByQuery('people', query)

		for item in data['hits']['hits']:
			people = item['_source']

			logger.info("processing %s login" % people['login'])

			## search technologies from login
			(techs, status_code) = tc.profile(people['login'])
			
			if status_code != 200:
				logger.warn("%s not has login on Tech Gallery" % people['login'])
				continue

			if 'technologies' in techs:
				for tech in techs['technologies'] :
					doc = {
				       'login': people['login'],
				       'name' : people['name'],		       
				       'role' : people['role']['name'],
				       'city' : people['cityBase']['acronym'],
				       'project' : people['project']['name'],
				       'area' : people['area']['name'],
				       'technologyName': tech['technologyName'],
				       'endorsementsCount' : tech['endorsementsCount'],
				       'skillLevel' : tech['skillLevel']
					}
					
					## create index doc
					repository.createTemplateIfNotExits('skill')
					repository.saveDocument('skill', 'technology', doc)


	def delete_sheet(self, sheet_id):
		repository = self.repository
		q = "sheet_id:"+sheet_id
		repository.deleteByQuery('project', q)					
		## delete sheet_id from knowledge
		repository.deleteByQuery('knowledge', q)
		repository.deleteByQuery('stack', 'key:'+sheet_id)

	
	# https://developers.google.com/sheets/reference/rest/v4/spreadsheets/get
	def load_knowledge_map(self, sheet=None, notify=False):
		knowledge = self.knowledge
		repository = self.repository
		
		# authenticate and get service API for spreadsheet
		service = knowledge.get_service_spreadsheets()


		if sheet:
			query = {"query": {"match": {"sheet_id": sheet}}}
		else:
			query = {"query": {"match_all": {}}}

		#spreadsheets = '1uzyIZf2r3DLKptr8ikeym1NNwiav-BwmtX3qbtDzhA4,1bPKnCx9nhcpEHoY9iMsW3LSDe5cORlkV2eLmHr6Wl5Y'.split(',')
		spreadsheets = repository.searchByQuery('project', query)

		total_hits = spreadsheets['hits']['total']
		print 'total %s sheets' % total_hits
		total_errs = 0

		for item in spreadsheets['hits']['hits']:
			spreadsheetId = item['_source']['sheet_id']
			owner = item['_source']['update_by']
			flow = item['_source']['flow']			
			contract = item['_source']['contract']
			logger.debug('processing spreadsheet: %s ' % spreadsheetId) 
			rangeName = 'TC_Report!A2:K'

			values = []
			try:
				result = service.spreadsheets().values().get(spreadsheetId=spreadsheetId, range=rangeName).execute()
				values = result.get('values', [])          

				if not values:
					logger.warn('No data found.')
				else:
					items = knowledge.readSheetData(spreadsheetId, values)					
					logger.debug('%s technologies on this spreadsheet ' % len(items))

					q = "sheet_id:"+spreadsheetId
					repository.deleteByQuery('knowledge', q)

					repository.createTemplateIfNotExits('knowledge')
					repository.saveDocuments('knowledge', 'tech', items)
					logger.info('==> spreadsheet %s loads successfully ' % spreadsheetId)
			except errors.HttpError, err:
				if err.resp.status in [404, 500]:
					# delete sheet_id from index project
					q = "sheet_id:"+spreadsheetId
					repository.deleteByQuery('project', q)					
					## delete sheet_id from knowledge
					repository.deleteByQuery('knowledge', q)
					logger.warning("==> Spreadsheet %s doesn't exists: %s" % (spreadsheetId, err))
				else:
					## send email to owner
					total_errs += 1
					logger.error("==> exception on %s : %s" % (spreadsheetId, err))
					if notify:
						subject = 'ACTION REQUIRED: Tech Gallery %s-%s' % (contract, flow)
						send_gmail.send(owner, subject, spreadsheetId, str(err))
			except Exception, e:
				total_errs += 1
				logger.error("==> exception on %s : %s" % (spreadsheetId, e))
				if notify:
					subject = 'ACTION REQUIRED: Tech Gallery %s-%s' % (contract, flow)
					send_gmail.send(owner, subject, spreadsheetId, str(e))
		# finished output log 
		logger.info('%s spreadsheets with %s errors' % (total_hits, total_errs))


	# https://developers.google.com/sheets/reference/rest/v4/spreadsheets/get
	def load_sheet_knowledge_map(self, spreadsheet):		
		knowledge = self.knowledge
		repository = self.repository
		
		# authenticate and get service API for spreadsheet
		service = knowledge.get_service_spreadsheets()

		item = spreadsheet

		spreadsheetId = item['_source']['sheet_id']
		owner = item['_source']['update_by']
		last_activity = item['_source']['@timestamp']
		flow = item['_source']['flow']
		contract = item['_source']['contract']
		logger.debug('processing spreadsheet: %s ' % spreadsheetId) 
		rangeName = 'TC_Report!A2:K'

		values = []
		try:
			result = service.spreadsheets().values().get(spreadsheetId=spreadsheetId, range=rangeName).execute()
			values = result.get('values', [])          

			if not values:
				logger.warn('No data found.')
			else:
				items = knowledge.readSheetData(spreadsheetId, values)

				## refresh flow and contract values from TC_Report sheet
				flow = items[0]['flow']
				contract = items[0]['contract']

				logger.debug('%s technologies on this spreadsheet ' % len(items))

				q = "sheet_id:"+spreadsheetId
				repository.deleteByQuery('knowledge', q)

				repository.createTemplateIfNotExits('knowledge')
				repository.saveDocuments('knowledge', 'tech', items)
				logger.info('==> spreadsheet %s loads successfully ' % spreadsheetId)
		except errors.HttpError, err:
			## send email to owner
			logger.error("==> exception on %s : %s" % (spreadsheetId, err))
			subject = 'ACTION REQUIRED: Tech Gallery %s-%s' % (contract, flow)
			send_gmail.send(owner, subject, spreadsheetId, str(err))
		except Exception, e:
			logger.error("==> exception on %s : %s" % (spreadsheetId, e))
			subject = 'ACTION REQUIRED: Tech Gallery %s-%s' % (contract, flow)
			send_gmail.send(owner, subject, spreadsheetId, str(e))

		doc = {
			"key": spreadsheetId,
			"owner" : contract,
			"name" : flow,
			"last_activity_user": owner,
			"last_activity" : last_activity,
			"index" : 0
		}

		return doc

class Repository(object):

	def __init__(self, config):
		self.config = config
		logger.debug('Connection on %s' % config['elasticsearch'])
		self.es = Elasticsearch([config['elasticsearch']['host']])	

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
	
	
	def searchByQuery(self, index, query):
		"""
		Sample of query: {"query": {"match_all": {}}}
		see more details on https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl.html
		"""
		resp = self.es.search(index=index, body=query, size=2500)
		logger.debug("%d documents found" % resp['hits']['total'])
		
		return resp
		
	def saveDocument(self, index, document_type, document, id=None):
		res = self.es.index(index=index, doc_type=document_type, body=document, id=id)
		logger.debug("Created documento ID %s" % res['_id'])

	#def savaDocuments(self):
		# bulk insert doc
		#print doc
		#docs.append(doc)
		#res = es_target.bulk(index="tc", doc_type="skill", body=doc, id_field='id', parent_field='_parent')
		#print("Bulk index " % res)	
	def saveDocuments(self, index, document_type, documents):
		for doc in documents:     
			## create index doc
			res = self.es.index(index=index, doc_type="tech", body=doc)
	      	 
	def deleteByQuery(self, index, search, number=10):     
		# Start the initial search. 
		hits = self.es.search(q=search, index=index, fields="_id",size=number,search_type="scan",scroll='5m')
		logger.debug('Deleting %s records... ' % hits['hits']['total'])

		# Now remove the results. 
		while True:
			try: 
				# Git the next page of results. 
				scroll = self.es.scroll( scroll_id=hits['_scroll_id'], scroll='5m', )

				# We have results initialize the bulk variable. 
				bulk = ""

				# Remove the variables. 
				for result in scroll['hits']['hits']:
					bulk = bulk + '{ "delete" : { "_index" : "' + str(result['_index']) + '", "_type" : "' + str(result['_type']) + '", "_id" : "' + str(result['_id']) + '" } }\n'

					self.es.bulk(body=bulk)
			except Exception, e: 
				break