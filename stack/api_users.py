from stack import app
from stack.security import login_required, validate_token
from flask import request, session, Response
from urllib2 import Request, urlopen, URLError


@app.route('/api/users/logged')
@login_required
def api_user_info():
    access_token = session.get('access_token')
    access_token = access_token[0]
    oauth_token = 'OAuth %s' % access_token
    headers = {'Authorization': oauth_token}
    print('==> Access Token - %s' % oauth_token)

    req = Request('https://www.googleapis.com/oauth2/v2/userinfo', None, headers)
    try:
        res = urlopen(req)
    except URLError, e:
        if e.code == 401:
            # Unauthorized - bad token
            print ('Unauthorized - bad token')
            session.pop('access_token', None)
            return redirect(url_for('login'))
        return res.read()

    return Response(response=res.read(),
                  status=200,
                  mimetype="application/json", headers=headers)

@app.route('/api/users/defails')
def api_user_detail():
    access_token = session.get('access_token')
    access_token = access_token[0]
    oauth_token = 'OAuth %s' % access_token

    userid = validate_token(oauth_token)
    print userid

    return userid

