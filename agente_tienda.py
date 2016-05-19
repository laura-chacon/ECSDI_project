from flask import Flask, request
from rdflib import Graph
from rdflib import URIRef, BNode, Literal, Namespace, RDF
from rdflib.namespace import FOAF
from rdflib.namespace import XSD
import rdflib

app = Flask(__name__)


@app.route('/busqueda_productos')

def busqueda_productos():
  
  params = request.args.get('categoria')
  g = Graph()
  try:
    g.parse('basededatos1.owl', format='xml')
  except Exception,e:
    print str(e)
  result = []
  n = Namespace('http://www.owl-ontologies.com/ECSDI/projectX.owl#')
  try:
    if params == ('Cosmetica'):
      prod = g.triples((None,RDF.type, n.Cosmetica))
      for s,p,o in prod:
	nprod = g.triples((s,n.nombre,None))
	for s, p, o in nprod:
	  result.append(str(o.toPython()))
    elif params == ('Electronica'):
      prod = g.triples((None,RDF.type, n.Electronica))
      for s,p,o in prod:
	nprod = g.triples((s,n.nombre,None))
	for s, p, o in nprod:
	  result.append(str(o.toPython()))
    elif params == ('Ropa'):
      prod = g.triples((None,RDF.type, n.Ropa))
      for s,p,o in prod:
	nprod = g.triples((s,n.nombre,None))
	for s, p, o in nprod:
	  result.append(str(o.toPython()))
    
    else:
      return 'No Category Match'
  
  except Exception,e: 
    print str(e)
    
  return str(result)

@app.route('/allproducts')

def all_products():
  
  params = request.args.get('categoria')
  g = Graph()
  try:
    g.parse('basededatos1.owl', format='xml')
  except Exception,e:
    print str(e)
  result = []
  n = Namespace('http://www.owl-ontologies.com/ECSDI/projectX.owl#')
  try:
    prod = g.triples((None,RDF.type, n.Cosmetica))
    for s,p,o in prod:
      nprod = g.triples((s,n.nombre,None))
      for s, p, o in nprod:
	result.append(str(o.toPython()))
    prod = g.triples((None,RDF.type, n.Electronica))
    for s,p,o in prod:
      nprod = g.triples((s,n.nombre,None))
      for s, p, o in nprod:
	result.append(str(o.toPython()))
    prod = g.triples((None,RDF.type, n.Ropa))
    for s,p,o in prod:
      nprod = g.triples((s,n.nombre,None))
      for s, p, o in nprod:
	result.append(str(o.toPython()))	  
  except Exception,e: 
    print str(e)
    
  return str(result)


if __name__ == '__main__':
  app.run(host='127.0.0.1', port=9001)