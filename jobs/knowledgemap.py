from __future__ import print_function
import logging
import os

import httplib2
from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools


logger = logging.getLogger('techanalytics')

SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
CLIENT_SECRET_FILE = 'resources/client_secret.json'
APPLICATION_NAME = 'Google Sheets API Python Quickstart'

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None


class KnowledgeMap(object):


    def __init__(self, config):
        self.config = config

    """ Class to manage all operations of people. This class expect a 
    config like this:

    If modifying these scopes, delete your previously saved credentials
    at ~/.credentials/sheets.googleapis.com-python-quickstart.json
    """

    def get_credentials(self):
        """Gets valid user credentials from storage.

        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.

        Returns:
            Credentials, the obtained credential.
        """
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir, 'sheets.googleapis.com-python-quickstart.json')

        store = oauth2client.file.Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            resource_path = os.path.join(os.path.split(__file__)[0], CLIENT_SECRET_FILE)
            flow = client.flow_from_clientsecrets(resource_path, SCOPES)
            flow.user_agent = APPLICATION_NAME
            if flags:
                credentials = tools.run_flow(flow, store, flags)
            else: # Needed only for compatibility with Python 2.6
                credentials = tools.run(flow, store)
            print('Storing credentials to ' + credential_path)

        return credentials


    # return float number. if exists ',' character, it will be change to '.'' 
    def formatFloat(self, value):
        if value.find(',') == -1: 
            # convert string br to float
            return float(value) 
        else:
            return float(value.replace(',','.'))


    def readSheetData(self, spreadsheetId, values):
        items = []
        for row in values:
          # Print columns A and E, which correspond to indices 0 and 4.
          doc = {
             'technology': row[0],
             'tower': row[1],            
             'contract': row[2],
             'flow': row[3],
             'gap': int(row[4]),
             'weight': int(row[5]),
             'necessity': int(row[6]),
             'requirement': int(row[7]),
             'relevancy': self.formatFloat(row[8]),
             'skill_index': self.formatFloat(row[9]),
             'achieve': int(row[10]),
             'sheet_id': spreadsheetId
          }
          items.append(doc)
        return items

    
    def get_service_spreadsheets(self):
        """Shows basic usage of the Sheets API.

        Creates a Sheets API service object and prints lines of a sample spreadsheet:
        https://docs.google.com/spreadsheets/d/1uzyIZf2r3DLKptr8ikeym1NNwiav-BwmtX3qbtDzhA4/edit
        """
        
        credentials = self.get_credentials()
        http = credentials.authorize(httplib2.Http())
        discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?version=v4')
        service = discovery.build('sheets', 'v4', http=http, discoveryServiceUrl=discoveryUrl)

        return service