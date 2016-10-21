from flask import render_template
from stack import app 
from flask import jsonify
from repository import Repository

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/stack/<id>')
def json_api(id):
	print ('Stack id %s' % id)

	r = Repository({'elasticsearch':'http://104.197.92.45:9200'})
	techs = r.search_technologies()
	
	return jsonify(techs)