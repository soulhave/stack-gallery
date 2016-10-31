from stack import app 
from security import login_required, login_authorized, validate_token, revoke_token

from flask import Flask, redirect, url_for, session
from flask import render_template
from flask import request, abort
from flask_oauth import OAuth


# You must configure these 3 values from Google APIs console
# https://code.google.com/apis/console
## tech-analytics client-id
##GOOGLE_CLIENT_ID = '146680675139-6fjea6lbua391tfv4hq36hl7kqo7cr96.apps.googleusercontent.com'
##GOOGLE_CLIENT_SECRET = 'iRZziZaSswbv3y_zAOkk1AS4'
## tech-gallery client-idfrom flask import request
GOOGLE_CLIENT_ID = '146680675139-6fjea6lbua391tfv4hq36hl7kqo7cr96.apps.googleusercontent.com'
GOOGLE_CLIENT_SECRET = 'iRZziZaSswbv3y_zAOkk1AS4'
REDIRECT_URI = 'authorized'  # one of the Redirect URIs from Google APIs console

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


@app.route('/signin')
def signin():
    return render_template('login.html')

@app.route('/login')
def login():
    callback=url_for(REDIRECT_URI, _external=True)
    return google.authorize(callback=callback)

@app.route('/logout')
def logout():
    access_token = session.get('access_token')
    print 'access_token %s' % access_token[0] 
    session.pop('access_token', None)

    revoke_token(access_token[0])

    return redirect(url_for('index'))

@app.route('/%s'% REDIRECT_URI)
@google.authorized_handler
def authorized(resp):
    access_token = resp['access_token']
    print ('token ===> %s' % access_token)

    access_token = access_token
    oauth_token = 'OAuth %s' % access_token    
    userid = validate_token(oauth_token)
    print ('userid ==> %s' % userid)

    if not '@ciandt.com' in userid:
      abort(403)
    else:  
      session['access_token'] = access_token, ''
      return redirect(url_for('index'))

@google.tokengetter
def get_access_token():
    return session.get('access_token')