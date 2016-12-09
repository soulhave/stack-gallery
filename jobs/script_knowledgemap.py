import logging
import os
import sys
from client import TechAnalytics

FORMAT = '%(name)s %(levelname)-5s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger('stack')
logger.addHandler(logging.NullHandler())
logger.setLevel(logging.DEBUG)
logging.getLogger('elasticsearch').setLevel(logging.ERROR)

ta = TechAnalytics()
sheet = None
#sheet = '1I7-yufu3vUHhj0RQO6ssQbLDsvf5GuFk8bqlhTTdk-4'

ta.load_knowledge_map(sheet=sheet, notify=True)