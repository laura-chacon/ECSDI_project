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

def newInfo(numpedido, nombreComprador, direccionComprador, totalCompra, cuentaComprador, tipo):
	try:
		info ={"numpedido": numpedido, "nombreComprador": nombreComprador, "direccionComprador": direccionComprador, "totalCompra": totalCompra, "cuentaComprador": cuentaComprador, "tipo": tipo}
		infoBanco.append(info)
	except Exception, e:
		print str(e)

def deleteInfo(numpedido):
	try:
		for i in infoBanco:
			if(i['numpedido'] == numpedido):
				infoBanco.remove(i)
		print infoBanco
	except Exception, e:
		print str(e)


@app.route('/realizarTransaccion', methods=['GET', 'POST'])
def  realizarTransaccion():
	try:
		if request.method == 'POST':
			global infoBanco
			print 'VOY A COBRARTE'
			print request.data
			info = json.loads(request.data)
			numpedido = info['numpedido']
			print numpedido
			nombreComprador = info['nombreComprador']
			print nombreComprador
			direccionComprador = info['direccionComprador']
			print direccionComprador
			totalCompra = info['totalCompra']
			print totalCompra
			cuentaComprador = info['cuentaComprador']
			tipo = info['tipo']
			newInfo(numpedido, nombreComprador, direccionComprador, totalCompra, cuentaComprador, tipo)
			'''EL BANCO TE COBRA'''
			return 'OK'
		if request.method == 'GET':
			'''infoparams = {"info": json.dumps(infoBanco)}'''
			return render_template('cobrarPedido.html', params=infoBanco)
	except Exception, e:
	    print str(e)
    	return 'Bad'

@app.route('/pedidoCobrado', methods=['GET'])
def pedidoCobrado():
	try:
		print 'YA LO COBRE'
		numpedido = request.args.get("numpedido", type=int)
		tipo = request.args.get("tipo")
		print str(numpedido)
		print tipo
		peticion = {"numeroPedido": numpedido, "tipo": tipo}
		r = requests.post('http://127.0.0.1:9001/cobroRealizado',data = json.dumps(peticion))
		deleteInfo(numpedido)
		return 'OK'
	except Exception, e:
		print str(e)
		print 'Bad'
  

if __name__ == '__main__':
  app.run(host='127.0.0.1', port=9003)