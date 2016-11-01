from flask import redirect, url_for, session
from flask import request, abort
from functools import wraps
from httplib2 import Http
import json

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        access_token = session.get('access_token')
        print ( '==> login_required access_token: ' + str(access_token))
        if access_token is None:
          print ('==> not logged')
          # use for add feature redirect to next-url - redirect(url_for('signin', next=request.url))
          return redirect(url_for('signin'))
        return f(*args, **kwargs)
    return decorated_function

def login_authorized(fn):
    """Decorator that checks that requests
    contain an id-token in the request header.
    userid will be None if the
    authentication failed, and have an id otherwise.

    Usage:
    @app.route("/")
    @auth.login_authorized
    def secured_call(userid=None):
        pass
    """
    @wraps(fn)
    def decorated_function(*args, **kwargs):
        if 'Authorization' not in request.headers:
            # Unauthorized
            print("No token in header")
            abort(401)
            return None

        print("Checking token...")
        authorization = request.headers['Authorization']
        print ('==> %s' % authorization )
        user = validate_token(authorization)
        if user is None:
            print("Check returned FAIL!")
            # Unauthorized
            abort(401)
            return None
        return fn(user=user, *args, **kwargs)
    return decorated_function    


def revoke_token(access_token):
    h = Http()
    print ('revoking %s' % access_token)
    resp, cont = h.request('https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token,
                           headers={'Host': 'www.googleapis.com',
                                    'Authorization': access_token})

    print cont

    return resp


# put this in for example gauth.py
# ref: http://flask.pocoo.org/snippets/125/
def validate_token(access_token):
    '''Verifies that an access-token is valid and
    meant for this app.

    Returns None on fail, and an User on success'''
    h = Http()
    resp, cont = h.request("https://www.googleapis.com/oauth2/v2/userinfo",
                           headers={'Host': 'www.googleapis.com',
                                    'Authorization': access_token})

    print cont

    if not resp['status'] == '200':
        return None

    try:
        data = json.loads(cont)
    except TypeError:
        # Running this in Python3
        # httplib2 returns byte objects
        data = json.loads(cont.decode())

    data['oauth_token'] = access_token

    return data