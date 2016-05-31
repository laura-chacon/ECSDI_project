from flask import Flask, jsonify, render_template, request, url_for
import requests
import json
from rdflib import Graph
from rdflib import URIRef, BNode, Literal, Namespace, RDF
from rdflib.namespace import FOAF
from rdflib.namespace import XSD
import rdflib

app = Flask(__name__)

g = Graph()
n = Namespace('http://www.owl-ontologies.com/ECSDI/projectX.owl#')

@app.route('/venderProductoExterno', methods=['GET'])
def venderProductoExterno():
    try:
        result = []
        g.parse('prueba.rdf', format='xml')
    except Exception,e:
        print str(e)
    try:
        vendedor_externo = g.triples((None, RDF.type, n.VendedorExterno))
        for s,p,o in vendedor_externo:
            nombre_vendedor_externo = g.triples((s, n.nombre, None))
            for s,p,o in nombre_vendedor_externo:
                nombre = o.toPython()
                cuenta = g.value(s, n.cuentaBancaria)
                result.append({'nombre': nombre, 'cuentaBancaria': cuenta})
        return render_template('venderProductoExterno.html', nombre_vendedor_externo=result)
    except Exception, e:
        print str(e)

@app.route('/realizarPeticion', methods=['POST'])
def realizarPeticion():
    peticion = {}
    try:
        nombre_vendedor = request.form["nombres_vendedor"]
        producto = request.form["producto"]
        cuenta = request.form["cuentas"]
        precio = request.form["precio"]
        categoria = request.form["categoria"]
        peticion = {"nombre_vendedor": nombre_vendedor,
                    "producto": producto,
                    "precio": precio,
                    "cuenta": cuenta,
                    "categoria": categoria
        }
        r = requests.post('http://127.0.0.1:9001/acordarProductoExterno', data=json.dumps(peticion))
        return "peticion done"
    except Exception, e:
        print str(e)

@app.route('/gestionarPedidoExterno')
def gestionarPedidoExterno():
    try:
        return render_template('gestionarPedidoExterno.html')
    except Exception, e:
        print str(e)

if __name__ == '__main__':
  app.run(host='127.0.0.1', port=9002)
