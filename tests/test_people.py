from preggy import expect

from tests.base import TestCase
from techanalytics import config
from techanalytics.people import People

class ConfigTestCase(TestCase):
    def test_has_people_load(self):
    	c = config.load()
    	p = People(c['people'])
    	list_people = p.loadAll()
    	expect(len(list_people)).to_be_greater_than(0)
    		
    def test_has_project_not_empty(self):
			c = config.load()
			p = People(c['people'])
			list_people = p.loadAll()
			if list_people:
				project = p.loadProjectFromHtml(list_people[0])
				expect(project).not_to_be_empty()
			else:
				expect.not_to_be_here() 

    def test_has_project_not_empty(self):
			c = config.load()
			p = People(c['people'])
			project = p.loadProjectFromHtml('blablabla')
			expect(project).to_equal('Empty')