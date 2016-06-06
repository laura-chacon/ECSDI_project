from flask import Flask, request, render_template, url_for
from rdflib import Graph
from rdflib import URIRef, BNode, Literal, Namespace, RDF
from rdflib.namespace import FOAF
from rdflib.namespace import XSD
import json
import rdflib
import requests
import logging

app = Flask(__name__)

'''logging.basicConfig()'''

g = Graph()
n = Namespace('http://www.owl-ontologies.com/ECSDI/projectX.owl#')
peticion = {"nombre_vendedor": None,
            "producto": None,
            "precio": None,
            "cuenta": None,
            "categoria": None
          }

pedidosPorProcesar = []

@app.route('/derivarPedido')
def derivarPedido():
 try:
	pedido = json.loads(requests.data)
	pedidosPorProcesar.append(pedido)
	return 'OK'
 except Exception,e:
	return 'Bad'

@app.route('/realizarEnvios')
def realizarEnvios():

    g.parse('prueba.rdf', format='xml')
    try:
	pedidos = []
	for pet in pedidosPorProcesar:
		peticion = {"numPedido": pet['numPedido'], "dirreccion": pet['dirreccion'], "nombreUsuario": pet["nombreUsuario"]}
		pedidos.append(peticion)
	nombreTransportistas = []
	transportistas = g.triples((n, RDF.type, n.Transportista))
	for s,p,o in transportistas:
		nombreTrans = g.triples((s, n.nombre, None))
		transportista = {"nombre": o.ToPython()}
		nombreTransportistas.append(transportista)
	return render_template('envios.html', transportistas=json.dumps(nombreTransportistas), pedidos=json.dumps(pedidos))
     except Exception,e:
	return 'Bad'

@app.route('/pedidoEnviado')
def confirmarPedido():
   try:
	pedido = json.loads(requests.data);
	r = requests.get('http://127.0.0.1:9001/pedidoEnviado', data=json.dumps(pedido))
	return 'OK'
   except Exception,e:
	return 'Bad'

if __name__ == '__main__':
  app.run(host='127.0.0.1', port=9004)    



