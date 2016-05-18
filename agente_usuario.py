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
  g = Graph()
  print ('antes del load')
  try:
    g.parse('basededatos1.owl', format='xml')
  except Exception,e:
    print str(e)
  print ('hemos cargado el grafo')
  n = Namespace('http://www.owl-ontologies.com/ECSDI/projectX.owl#')
  
  #Para buscar con g.triples se necesita especificar el tipo de XML SCHEMA que es: int, string, etc... Mirarse en el .owl
  try:
    z = g.triples((None, n.nombre,Literal('Esther', datatype= XSD.string)))
    for _,_,o in z:
      print type(o)
      print o
      if (Literal(23).eq(o)):
	print('equal')
	
  except Exception,e: 
    print str(e)
  peticion = {'categoria': 'electronica'}
  r = requests.get('http://127.0.0.1:9001/busqueda_productos', params=peticion)
  return r.text


if __name__ == '__main__':
  app.run(host='127.0.0.1', port=9000)
