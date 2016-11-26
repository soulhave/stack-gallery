import logging
import os

import requests
import urlparse
from requests.auth import HTTPBasicAuth
from lxml import html

logger = logging.getLogger('techanalytics')

class People(object):
	""" Class to manage all operations of people. This class expect a 
	config like this:
		people: 
		  people:
		    url: https://people.cit.com.br
		    user: 
		    pass:
		  gateway:
		    url: https://wsgateway.cit.com.br
		    app_token: Blpy2nNXnjya
		  elasticsearch:
		    url: http://104.197.92.45:9200	

	people.user and people.pass can be override using environment variables
 		os.environ.get('PEOPLE_USER',config['people']['user'])

	p = People(config)
	"""

	def __init__(self, config):
		self.config = config
		self.people_host = config['people']['host']
		self.username = os.environ.get('PEOPLE_USER',config['people']['user'])
		self.password = os.environ.get('PEOPLE_PASS',config['people']['pass'])

	def loadProjectFromHtml(self, login):
		"""Scan project name from people system using login as parameter 

		Args:
		      login: Username for build url https://people.cit.com.br/profile/+login
		"""			
		url = '%s/profile/%s' % (self.people_host, login) 
		response = requests.get(url=url, auth=HTTPBasicAuth(self.username, self.password))

		# Response
		logger.debug(url)
		if response.status_code != 200:
			logger.error("fail to load project name for %s. Check people username and password" % login)
			return "Empty"

		parsed_body = html.fromstring(response.text)
		elements =  parsed_body.xpath('.//div[@class="user-projects"]//ul//li[1]//a')
		
		if elements:
			return elements[0].text_content()
		return "Empty"


	def loadAll(self):
		"""Return all ative users from people system. 

		Args:
		      app_token: it is a token form api gateway. You need to request one 
		      for you if you want call this API
		"""	

		token = os.environ.get('GATEWAY_TOKEN', self.config['gateway']['app_token'])
		headers = {'app_token': token}

		url = '%s/cit/api/v2/people/' % self.config['gateway']['host']

		response = requests.get(url=url, headers=headers)
		
		logger.info(response.status_code)
		logger.debug( response.headers)

		return response.json()

	def dumpImage(self, login):
		url = '%s/profile/%s' % (self.people_host, login) 
		response = requests.get(url=url, auth=HTTPBasicAuth(self.username, self.password))

		parsed_body = html.fromstring(response.text)

		# Grab links to all images
		images = parsed_body.xpath('.//div[@class="container"]/div[@class="photo"]/img/@src')

		if images:  
			# Convert any relative urls to absolute urls
			images = [urlparse.urljoin(response.url, url) for url in images]  
			logger.info('Found %s images' % len(images))

			# Only download first 10
			for url in images[0:10]:  
			    r = requests.get(url, auth=HTTPBasicAuth(self.username, self.password))
			    f = open('downloaded_images/%s' % url.split('/')[-1], 'w')
			    f.write(r.content)
			    f.close()