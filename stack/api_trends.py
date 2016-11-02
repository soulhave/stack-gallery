from stack import app
from stack.security import login_authorized

import requests
from flask import jsonify

@app.route('/api/trends/owners')
@login_authorized
def api_trends_owners(user):

  data = [
    {
      'name' : 'itau',
      'count' : 10
    },
    {
      'name' : 'google',
      'count' : 6
    },
    {
      'name' : 'vale',
      'count' : 2
    }        
  ]

  return jsonify(data)


@app.route('/api/trends/technologies')
@login_authorized
def api_trends_technologies(user):

  data = [
    {
      'name' : 'git',
      'count' : 20
    },
    {
      'name' : 'java',
      'count' : 6
    },
    {
      'name' : 'python',
      'count' : 2
    },
    {
      'name' : 'java script',
      'count' : 20
    },
    {
      'name' : 'Angular JS',
      'count' : 6
    },
    {
      'name' : 'Mongo DB',
      'count' : 22
    }         
  ]

  return jsonify(data)
