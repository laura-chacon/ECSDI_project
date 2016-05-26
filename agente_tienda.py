from flask import Flask, request
from rdflib import Graph
from rdflib import URIRef, BNode, Literal, Namespace, RDF
from rdflib.namespace import FOAF
from rdflib.namespace import XSD
import json
import rdflib

app = Flask(__name__)

g = Graph()
n = Namespace('http://www.owl-ontologies.com/ECSDI/projectX.owl#')



def precioEnIntervalo(precio, filtradoDePrecio):
  if filtradoDePrecio == "De0a30":
    if precio >= 0 and precio <= 30: 
      return True
  if filtradoDePrecio == "De30A100":
    if precio > 30 and precio <= 100:
      return True
  if filtradoDePrecio == "MayorA100":
    if precio > 100:
      return True
  else:
    return False
  
def obtenerNombre(sujeto):
  nprod = g.triples((sujeto,n.nombre,None))
  nombre = ''
  for s, p, o in nprod:
    nombre = o.toPython()
  return nombre



@app.route('/busqueda_productos')

def busqueda_productos():
  try:
    params = json.loads(request.data)
    g.parse('basededatos1.owl', format='xml')
  except Exception,e:
    print str(e)
  result = []
  isCategorySelected = 0
  
  #Filtrado de precio
  precioFiltrado = params["Precio"]
  filtradoDePrecio = ""
  
  if precioFiltrado["De0a30"] == 1:
    filtradoDePrecio = "De0a30"
  if precioFiltrado["De30A100"] == 1:
    filtradoDePrecio = "De30A100"
  if precioFiltrado["MayorA100"] == 1:
    filtradoDePrecio = "MayorA100"
  
  
  n = Namespace('http://www.owl-ontologies.com/ECSDI/projectX.owl#')
  try:
    params = params['Categoria']
    if params["Cosmetica"] == 1:
      if isCategorySelected == 0:
	isCategorySelected = 1
      prod = g.triples((None,RDF.type, n.Cosmetica))
      for s,p,o in prod:
	nprod = g.triples((s,n.nombre,None))
	nombre = ''
	for s, p, o in nprod:
	  nombre = o.toPython()
	  precio = 0
	  nprec = g.triples((s,n.precio, None))
	  for s, p, o in nprec:
	    precio = o.toPython()
	    if filtradoDePrecio != "":
	      if precioEnIntervalo(precio,filtradoDePrecio):
		result.append({'nombre': nombre, 'precio': precio})
	    else:
	      result.append({'nombre': nombre, 'precio': precio})
    if params["Electronica"] == 1:
      if isCategorySelected == 0:
	isCategorySelected = 1
      prod = g.triples((None,RDF.type, n.Electronica))
      for s,p,o in prod:
	nprod = g.triples((s,n.nombre,None))
	nombre = ''
	for s, p, o in nprod:
	  nombre = o.toPython()
	  precio = 0
	  nprec = g.triples((s,n.precio, None))
	  for s, p, o in nprec:
	    precio = o.toPython()
	    if filtradoDePrecio != "":
	      if precioEnIntervalo(precio,filtradoDePrecio):
		result.append({'nombre': nombre, 'precio': precio})
	    else:
	      result.append({'nombre': nombre, 'precio': precio})  
    if params["Ropa"] == 1:
      if isCategorySelected == 0:
	isCategorySelected = 1
      prod = g.triples((None,RDF.type, n.Ropa))
      for s,p,o in prod:
	nprod = g.triples((s,n.nombre,None))
	nombre = ''
	for s, p, o in nprod:
	  nombre = o.toPython()
	  precio = 0
	  nprec = g.triples((s,n.precio, None))
	  for s, p, o in nprec:
	    precio = o.toPython()
	    if filtradoDePrecio != "":
	      if precioEnIntervalo(precio,filtradoDePrecio):
		result.append({'nombre': nombre, 'precio': precio})
	    else:
	      result.append({'nombre': nombre, 'precio': precio})
	      
      
  except Exception,e: 
    print str(e)
  jsondata = json.dumps(result)
  return jsondata

@app.route('/allproducts')

def all_products():
  
  params = request.args.get('categoria')
  g = Graph()
  try:
    g.parse('basededatos1.owl', format='xml')
  except Exception,e:
    print str(e)
  result = []
  try:
    prod = g.triples((None,RDF.type, n.Cosmetica))
    for s,p,o in prod:
      nprod = g.triples((s,n.nombre,None))
      for s, p, o in nprod:
	nombre = o.toPython()
	nprec = g.triples((s,n.precio, None))
	precio = 0
	for s, p, o in nprec:
	  precio = o.toPython()
	result.append({'nombre': nombre, 'precio': precio})
    prod = g.triples((None,RDF.type, n.Electronica))
    for s,p,o in prod:
      nprod = g.triples((s,n.nombre,None))
      for s, p, o in nprod:
	nombre = o.toPython()
	nprec = g.triples((s,n.precio, None))
	precio = 0
	for s, p, o in nprec:
	  precio = o.toPython()
	result.append({'nombre': nombre, 'precio': precio})
    prod = g.triples((None,RDF.type, n.Ropa))
    for s,p,o in prod:
      nprod = g.triples((s,n.nombre,None))
      for s, p, o in nprod:
	nombre = o.toPython()
	nprec = g.triples((s,n.precio, None))
	precio = 0
	for s, p, o in nprec:
	  precio = o.toPython()
	result.append({'nombre': nombre, 'precio': precio})	  
  except Exception,e: 
    print str(e)
  jsondata = json.dumps(result)
  return jsondata


@app.route('/pedidos')

def pedidos():
  
  try:
    g.parse('basededatos1.owl', format='xml')
    compras = g.triples((None,RDF.type, n.Compra))
    for s,p,o in compras:
      print s,p,o
      enviado = g.triples((s,n.Contiene, None))
      for s,p,o in enviado:
	print "Sujeto"
	print s
	print "Predicado"
	print p
	print "Objeto"
	print o.toPython()
	producto = g.triples((o, n.nombre, None))
	for s,p,o in producto:
	  print "Nombre"
	  print o
      
    return 'OK'
  except Exception,e:
    print str(e)
    return 'Bad'





if __name__ == '__main__':
  app.run(host='127.0.0.1', port=9001)