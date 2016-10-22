import requests

#username = raw_input("Enter Username for basic auth. Default admin => ") or "admin"
#password = raw_input("Enter Password. Default admin => ") or "admin"

class TechGallery(object):
	""" 

	techgallery:
		endpoint: https://tech-gallery.appspot.com/_ah/api/rest/v1 
	"""
	def __init__(self, config):
		self.config = config
		self.endpoint = config['endpoint']

	def searchTechnologiesByLogin(self, login):
		url = '%s/profile?email=%s@ciandt.com' %(self.endpoint,login)
		# sample url 'https://tech-gallery.appspot.com/_ah/api/rest/v1/profile?email='+ login + '@ciandt.com'

		response = requests.get(url=url)

		return response;

	def technology(self, id):
		url = '%s/technology/%s' %(self.endpoint,id)
		response = requests.get(url=url)

		return response.json()
