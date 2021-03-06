from server import app, security, logger

from flask import jsonify
from flask import request
import requests
import json
import logging
from datetime import datetime


# Using OAuth 2.0 to Access Google APIs. Login flow
# https://developers.google.com/identity/protocols/OAuth2
# https://developers.google.com/identity/protocols/OpenIDConnect#exchangecode
# Step 1: (Browser) Send an authentication request to Google
# Step 2: Exchange authorization code for access token.
# Step 3: Retrieve information about the current user.
@app.route('/auth/google', methods=['POST'])
def google():
    access_token_url = 'https://www.googleapis.com/oauth2/v4/token'
    people_api_url = 'https://www.googleapis.com/oauth2/v3/userinfo'
    tokeninfo_url = 'https://www.googleapis.com/oauth2/v3/tokeninfo'

    logger.debug('google request =>')
    logger.debug(request.json)

    payload = dict(client_id=request.json['clientId'],
                   redirect_uri=request.json['redirectUri'],
                   client_secret=app.config['GOOGLE_CLIENT_SECRET'],
                   code=request.json['code'],
                   grant_type='authorization_code')

    logger.debug('Google Payload =>')
    logger.debug(payload)

    # Step 2. Exchange authorization code for access token.
    r = requests.post(access_token_url, data=payload)
    token = json.loads(r.text)
    logger.debug('Access Token =>')
    logger.debug(token)

    # Step 2. Retrieve information about the current user.
    # create user if not exists one
    headers = {'Authorization': 'Bearer {0}'.format(token['access_token'])}
    r = requests.get(people_api_url, headers=headers)
    profile = json.loads(r.text)
    logger.info('Login as => %s' % profile['email'])
    logger.debug(profile)

    if security.is_valid_email(profile['email']):
        # Step 4. Create a new account or return an existing one.
        r = requests.get('%s?access_token=%s' % (tokeninfo_url, token['access_token']))
        token_info = json.loads(r.text)
        logger.debug('Tokeninfo =>')
        logger.debug(token_info)

        # Step 5. Create a new account or return an existing one.
        payload = {
            'sub': profile['sub'],
            'iat': datetime.utcnow(),
            'exp': token_info['exp'],
            'access_token':token['access_token']
        }
        jwt = security.create_token(payload)
        return jsonify(token=jwt)
    else:
        return not_authorized(403, 'Invalid email domain. Please sign with ciandt.com acccount')


@app.route('/api/logout', methods=['GET'])
@security.login_authorized
def logout(user):
    logger.info('Logout by %s' % user['email'])
    access_token = user['oauth_token']
    security.revoke_token(access_token)

    return "Logout Success", 200

def not_authorized(status, error):
    response = jsonify({'code': status,'message': error})
    response.status_code = status
    return response

class User:
    def __init__(self, id, email=None, password=None, display_name=None,
                 provider=None):
        self.id = id
        if email:
            self.email = email.lower()
        if password:
            self.password = password
        if display_name:
            self.display_name = display_name
        if provider:
            self.provider = provider

    def to_json(self):
        return dict(id=self.id, email=self.email, displayName=self.display_name,
                    google=self.google)
