import requests

class TechGallery(object):
	""" 

	techgallery:
		endpoint: https://tech-gallery.appspot.com/_ah/api/rest/v1 
	"""
	def __init__(self, config):
		self.config = config
		self.endpoint = config['endpoint']

	def profile(self, login):
		url = '%s/profile?email=%s@ciandt.com' %(self.endpoint,login)
		response = requests.get(url=url)
		# TODO: throw exception if response.status_code <> 200
		return response.json(), response.status_code;

	def technology(self, id):
		url = '%s/technology/%s' %(self.endpoint,id)
		response = requests.get(url=url)

		return response.json(), response.status_code
