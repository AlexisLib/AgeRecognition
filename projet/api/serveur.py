#! /usr/bin/python
# -*- coding:utf-8 -*-
from myDB import MyDB
from flask import Flask, make_response
from flask_cors import CORS
import json


app = Flask(__name__)
CORS(app, supports_credentials=True)


@app.route('/dataset/')
def dataset():
	datas = {}
	try:
		with open('queries.json', 'r') as file:
			queries = json.load(file)
		print(type(queries))
	except:
		return make_response("Erreur fichier queries", 503)
	
	try:
		db = MyDB()
		for key, query in queries.items():
			db.query(query)
			datas[key] = db.fetchone()[0]
		
		return json.dumps(datas)

	except:
		return make_response("Erreur connexion bdd", 503)


@app.route('/results/')
def results():
	results = {}
	results["order"] = ["Modele lineaire", "PMC", "RBFN", "SVM"]
	results["implement"] = {"Modele lineaire": "NA", "PMC": "NA", "RBFN": "NA", "SVM":"NA"}
	results["framework"] = {"Modele lineaire": "NA", "PMC": "NA", "RBFN": "NA", "SVM":"NA"}
	return json.dumps(results)

if __name__ == '__main__':

    app.run(debug=True, host="0.0.0.0")
