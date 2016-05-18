from flask import Flask
import requests
from rdflib import Graph
from rdflib import URIRef, BNode, Literal, Namespace, RDF
from rdflib.namespace import FOAF

app = Flask(__name__)

@app.route('/busqueda')

def busqueda():
  g = Graph()
  print ('antes del load')
  g.load('basededatos1.owl', format='xml')
  print ('hemos cargado el grafo')
  n = Namespace('http://www.owl-ontologies.com/ECSDI/projectX.owl#')
  try:
    z = g.triples((None, n.precio, None))
    for s,p,o in z:
      print s, p, o
  except Exception,e: 
    print str(e)
  peticion = {'categoria': 'electronica'}
  r = requests.get('http://127.0.0.1:9001/busqueda_productos', params=peticion)
  return r.text


if __name__ == '__main__':
  app.run(host='127.0.0.1', port=9000)
