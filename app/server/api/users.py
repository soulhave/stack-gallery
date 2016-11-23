from server import app
from server import security

from flask import jsonify
from flask import request, session, Response

@app.route('/api/users/logged')
@security.login_authorized
def api_user_info(user):
    token = user['oauth_token']
    user.pop('oauth_token', None)

    response = jsonify(user)
    response.headers['Authorization'] = token

    return response

@app.route('/api/users/me')
@security.login_authorized
def api_user_detail(user):    
    return jsonify(user)