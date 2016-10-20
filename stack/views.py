from flask import render_template
from stack import app 
from flask import jsonify

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/stack/<id>')
def json_api(id):
	print ('Stack id %s' % id)

	pessoas = [
	{"nome": "Bruno Rocha"},
	{"nome": "Arjen Lucassen"},
	{"nome": "Anneke van Giersbergen"},
	{"nome": "Steven Wilson"}]
	
	return jsonify(pessoas)