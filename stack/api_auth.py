from stack import app
import security

from flask import jsonify
from flask import request
import requests
import json
import logging


from elasticsearch import Elasticsearch


@app.route('/auth/google', methods=['POST'])
def google():
    access_token_url = 'https://accounts.google.com/o/oauth2/token'
    people_api_url = 'https://www.googleapis.com/plus/v1/people/me/openIdConnect'

    payload = dict(client_id=request.json['clientId'],
                   redirect_uri=request.json['redirectUri'],
                   client_secret=app.config['GOOGLE_CLIENT_SECRET'],
                   code=request.json['code'],
                   grant_type='authorization_code')

    print payload

    # Step 1. Exchange authorization code for access token.
    r = requests.post(access_token_url, data=payload)
    token = json.loads(r.text)
    print token
    headers = {'Authorization': 'Bearer {0}'.format(token['access_token'])}

    # Step 2. Retrieve information about the current user.
    r = requests.get(people_api_url, headers=headers)
    profile = json.loads(r.text)

    print profile


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
