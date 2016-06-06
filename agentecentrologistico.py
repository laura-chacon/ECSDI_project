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

@app.route('/derivarPedido', methods=['POST'])
def derivarPedido():
 try:
    pedido = json.loads(request.data)
    pedidosPorProcesar.append(pedido)
    return 'OK'
 except Exception,e:
    return 'Bad'

@app.route('/realizarEnvios')
def realizarEnvios():

    g.parse('prueba.rdf', format='xml')
    try:
        pedidosList = []
        for pet in pedidosPorProcesar:
            print 'entramos'
            peticion = {'numPedido': pet['numPedido'], 'dirreccion': pet['dirreccion'], 'nombreUsuario': pet["nombreUsuario"]}
            pedidosList.append(peticion)
        nombreTransportistas = []
        ntrans = g.triples((None, RDF.type, n.Transportista))
        for s,p,o in ntrans:
            print 'entramos'
            nombreTrans = g.triples((s, n.nombre, None))
            for s, p, o in nombreTrans:
                transportista = {"nombre": o.toPython()}
                nombreTransportistas.append(transportista)
        pedidosPorProcesar = []
        return render_template('envios.html', trans = nombreTransportistas, pedidos= pedidosList)
    except Exception,e:
        print str(e)
        return 'Bad'

@app.route('/pedidoEnviado',  methods=['POST'])
def pedidoEnviado():
   try:
    pedido = {"nombreUsuario":"", "dirreccion" : "", "nombreTransportista": "", "fechaEntrega": "", "numeroPedido": ""}
    pedido['nombreUsuario'] = request.form['nombreUsuario']
    pedido['dirreccion'] = request.form['dirreccion']
    pedido['nombreTransportista'] = request.form['nombreTransportista']
    pedido['fechaEntrega'] = request.form['fechaEntrega']
    pedido['numeroPedido'] = request.form['numeroPedido']
    r = requests.post('http://127.0.0.1:9001/pedidoEnviado', data=json.dumps(pedido))
    return 'OK'
   except Exception,e:
    print str(e)
    return 'Bad'

if __name__ == '__main__':
  app.run(host='127.0.0.1', port=9004)    



