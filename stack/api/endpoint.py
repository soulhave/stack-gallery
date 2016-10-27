from stack import app 
from flask import jsonify
from stack.repository import Repository

@app.route('/api/stack', methods = ['GET'])
def api_stack():
	r = Repository({'elasticsearch':'http://104.197.92.45:9200'})
	techs = r.list_stack()
	
	return jsonify(techs)

@app.route('/api/team/<sheet_id>', methods = ['GET'])
def api_team(sheet_id):
	r = Repository({'elasticsearch':'http://104.197.92.45:9200'})
	team = r.list_team(sheet_id)
	
	return jsonify(team)