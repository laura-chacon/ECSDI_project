from flask import Flask, jsonify, render_template, request, url_for
import requests
import json
from rdflib import Graph
from rdflib import URIRef, BNode, Literal, Namespace, RDF
from rdflib.namespace import FOAF
from rdflib.namespace import XSD
import rdflib

app = Flask(__name__)


infoBanco = []

g = Graph()
n = Namespace('http://www.owl-ontologies.com/ECSDI/projectX.owl#')

@app.route('/realizarTransaccion', methods=['GET', 'POST'])
def  realizarTransaccion():
	try:
		if request.method == 'POST':
			global infoBanco
			print 'VOY A COBRARTE'
			print request.data
			infoBanco = json.loads(request.data)
			'''EL BANCO TE COBRA'''
			return 'OK'
		if request.method == 'GET':
			return render_template('cobrarPedido.html', params=infoBanco)
	except Exception, e:
	    print str(e)
    	return 'Bad'

@app.route('/pedidoCobrado', methods=['POST'])
def pedidoCobrado():
	try:
		print 'YA LO COBRE'
		print infoBanco['numpedido']
		r = requests.post('http://127.0.0.1:9001/cobroRealizado', data=str(infoBanco['numpedido']))
		return 'OK'
	except Exception, e:
		print str(e)
		print 'Bad'
  

if __name__ == '__main__':
  app.run(host='127.0.0.1', port=9003)