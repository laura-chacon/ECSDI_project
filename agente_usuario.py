from flask import Flask
import requests
from rdflib import Graph
from rdflib import URIRef, BNode, Literal, Namespace, RDF
from rdflib.namespace import FOAF
from rdflib.namespace import XSD
import rdflib

app = Flask(__name__)

@app.route('/busqueda')

def busqueda():
  peticion = {'categoria': 'Cosmetica'}
  r = requests.get('http://127.0.0.1:9001/busqueda_productos', params=peticion)
  print r
  return str(r.content)

@app.route('/catalog')

def catalog():
  r = requests.get('http://127.0.0.1:9001/allproducts')
  print r
  return str(r.content)

if __name__ == '__main__':
  app.run(host='127.0.0.1', port=9000)
