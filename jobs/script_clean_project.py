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
sheet_id = '1eQ2KJqddexCgVmiQRYEy1WtxcAA5cDpAA8ecveDsoNQ'

ta.delete_sheet(sheet_id=sheet_id)