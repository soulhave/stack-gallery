from flask import render_template
from stack import app 
from flask import jsonify
from repository import Repository

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dialog-team')
def dialog_team():
    return render_template('dialog-team.html')

@app.route('/stack')
def stack():
	r = Repository({'elasticsearch':'http://104.197.92.45:9200'})
	techs = r.search_stack()
	
	return jsonify(techs)


@app.route('/team/<sheet_id>')
def team(sheet_id):
	r = Repository({'elasticsearch':'http://104.197.92.45:9200'})
	team = r.list_team(sheet_id)
	
	return jsonify(team)	