from stack import app
import security

from flask import jsonify
from flask import request
import requests
import json
import logging


from elasticsearch import Elasticsearch

# Using OAuth 2.0 to Access Google APIs
# https://developers.google.com/identity/protocols/OAuth2


@app.route('/auth/google', methods=['POST'])
def google():
    access_token_url = 'https://www.googleapis.com/oauth2/v4/token'
    people_api_url = 'https://www.googleapis.com/oauth2/v3/userinfo'
    tokeninfo_url = 'https://www.googleapis.com/oauth2/v3/tokeninfo'

    print 'google request =>'
    print request.json

    payload = dict(client_id=request.json['clientId'],
                   redirect_uri=request.json['redirectUri'],
                   client_secret=app.config['GOOGLE_CLIENT_SECRET'],
                   code=request.json['code'],
                   grant_type='authorization_code')

    print 'Google Payload =>'
    print payload

    # Step 1. Exchange authorization code for access token.
    r = requests.post(access_token_url, data=payload)
    print r
    token = json.loads(r.text)
    print 'Token =>'
    print token

    # Step 2. Retrieve information about the current user.
    headers = {'Authorization': 'Bearer {0}'.format(token['access_token'])}
    r = requests.get(people_api_url, headers=headers)
    profile = json.loads(r.text)
    print 'Profile =>'
    print profile

    r = requests.get('%s?access_token=%s' % (tokeninfo_url, token['access_token']))
    token_info = json.loads(r.text)
    print 'Tokeninfo =>'
    print token_info

    # Step 4. Create a new account or return an existing one.
    u = User(id=token['access_token'], google=profile['sub'],
             display_name=profile['name'])
    jwt = security.create_token(u)
    print jwt
    return jsonify(token=jwt)


@app.route('/api/me')
@security.login_authorized
def me(user):
    return jsonify(user)


class User:
    def __init__(self, id, email=None, password=None, display_name=None,
                 google=None):

        self.id = id
        if email:
            self.email = email.lower()
        if password:
            self.password = password
        if display_name:
            self.display_name = display_name
        if google:
            self.google = google

    def to_json(self):
        return dict(id=self.id, email=self.email, displayName=self.display_name,
                    google=self.google)      
