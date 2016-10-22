from flask import Flask, redirect, url_for, session
from flask import request, abort
from flask import Response
from flask_oauth import OAuth
import requests
from httplib2 import Http
import json


# You must configure these 3 values from Google APIs console
# https://code.google.com/apis/console
## tech-analytics client-id
##GOOGLE_CLIENT_ID = '146680675139-6fjea6lbua391tfv4hq36hl7kqo7cr96.apps.googleusercontent.com'
##GOOGLE_CLIENT_SECRET = 'iRZziZaSswbv3y_zAOkk1AS4'
## tech-gallery client-idfrom flask import request
GOOGLE_CLIENT_ID = '146680675139-6fjea6lbua391tfv4hq36hl7kqo7cr96.apps.googleusercontent.com'
GOOGLE_CLIENT_SECRET = 'iRZziZaSswbv3y_zAOkk1AS4'

REDIRECT_URI = '/authorized'  # one of the Redirect URIs from Google APIs console

SECRET_KEY = 'development key'
DEBUG = True

app = Flask(__name__)
app.debug = DEBUG
app.secret_key = SECRET_KEY
oauth = OAuth()

google = oauth.remote_app('google',
                          base_url='https://www.google.com/accounts/',
                          authorize_url='https://accounts.google.com/o/oauth2/auth',
                          request_token_url=None,
                          request_token_params={'scope': 'https://www.googleapis.com/auth/userinfo.email',
                                                'response_type': 'code'},
                          access_token_url='https://accounts.google.com/o/oauth2/token',
                          access_token_method='POST',
                          access_token_params={'grant_type': 'authorization_code'},
                          consumer_key=GOOGLE_CLIENT_ID,
                          consumer_secret=GOOGLE_CLIENT_SECRET)

@app.route('/')
def index():
    access_token = session.get('access_token')
    if access_token is None:
        return 'Please <a href="/login">login</a>'
        #return redirect(url_for('login'))
    else:
      from urllib2 import Request, urlopen, URLError

      access_token = access_token[0]
      oauth_token = 'OAuth %s' % access_token
      headers = {'Authorization': oauth_token}
      print('==> Access Token - %s' % oauth_token)


      req = Request('https://www.googleapis.com/oauth2/v1/userinfo', None, headers)
      try:
          res = urlopen(req)
      except URLError, e:
          if e.code == 401:
              # Unauthorized - bad token
              print ('Unauthorized - bad token')
              session.pop('access_token', None)
              return redirect(url_for('login'))
          return res.read()

      resp = Response(response=res.read(),
                    status=200,
                    mimetype="application/json", headers=headers)

      return resp
      #return get_technology('angular_js', oauth_token)


# put this in for example gauth.py
# ref: http://flask.pocoo.org/snippets/125/
def validate_token(access_token):
    '''Verifies that an access-token is valid and
    meant for this app.

    Returns None on fail, and an e-mail on success'''
    h = Http()
    resp, cont = h.request("https://www.googleapis.com/oauth2/v2/userinfo",
                           headers={'Host': 'www.googleapis.com',
                                    'Authorization': access_token})

    if not resp['status'] == '200':
        return None

    try:
        data = json.loads(cont)
    except TypeError:
        # Running this in Python3
        # httplib2 returns byte objects
        data = json.loads(cont.decode())

    return data['email']

def authorized(fn):
    """Decorator that checks that requests
    contain an id-token in the request header.
    userid will be None if the
    authentication failed, and have an id otherwise.

    Usage:
    @app.route("/")
    @authorized
    def secured_root(userid=None):
        pass
    """

    def _wrap(*args, **kwargs):
        if 'Authorization' not in request.headers:
            # Unauthorized
            print("No token in header")
            abort(401)
            return None

        print("Checking token...")
        authorization = request.headers['Authorization']
        print ('==> %s' % authorization )
        userid = validate_token(authorization)
        if userid is None:
            print("Check returned FAIL!")
            # Unauthorized
            abort(401)
            return None

        return fn(userid=userid, *args, **kwargs)
    return _wrap

def get_technology(id, oauth_token):
  url = 'https://tech-gallery.appspot.com/_ah/api/rest/v1/technology/%s' % id
  headers = {'Authorization': oauth_token}
  response = requests.get(url=url, headers= headers)

  return response.text

@app.route('/technology/<id>')
@authorized
def list_technology(userid, id):
  print ('user - %s' % userid)
  #print (request.headers)
  url = 'https://tech-gallery.appspot.com/_ah/api/rest/v1/technology/%s' % id
  response = requests.get(url=url)

  return response.text

@app.route('/technologies')
def technologies():
  access_token = session.get('access_token')  
  url = 'https://tech-gallery.appspot.com/_ah/api/rest/v1/technology'

  oauth_token = 'OAuth ' + access_token[0]
  headers = {'Authorization': oauth_token}
  print('==> %s' % headers)
  response = requests.get(url=url, headers= headers)

  return response.text

@app.route('/login')
def login():
    callback=url_for('authorized', _external=True)
    return google.authorize(callback=callback)

@app.route('/logout')
def logout():
    session.pop('access_token', None)
    return redirect(url_for('index'))


@app.route(REDIRECT_URI)
@google.authorized_handler
def authorized(resp):
    access_token = resp['access_token']
    session['access_token'] = access_token, ''
    return redirect(url_for('index'))


@google.tokengetter
def get_access_token():
    return session.get('access_token')


def main():
    app.run()


if __name__ == '__main__':
    main()
