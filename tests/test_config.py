from preggy import expect

from tests.base import TestCase
from techanalytics import config

class ConfigTestCase(TestCase):
    def test_has_people_config(self):
    	c = config.load()	
    	people_host = c['people']['people']['host']
    	expect(people_host).to_equal('https://people.cit.com.br')
    		
