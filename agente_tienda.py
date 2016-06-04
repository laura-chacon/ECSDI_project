from flask import Flask, request, render_template, url_for
from rdflib import Graph
from rdflib import URIRef, BNode, Literal, Namespace, RDF
from rdflib.namespace import FOAF
from rdflib.namespace import XSD
import json
import rdflib
import requests

app = Flask(__name__)

g = Graph()
n = Namespace('http://www.owl-ontologies.com/ECSDI/projectX.owl#')
peticion = {"nombre_vendedor": None,
            "producto": None,
            "precio": None,
            "cuenta": None,
            "categoria": None
          }
'''variable global para asignar numero de pedido'''
numpedido = 500

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
    g.parse('prueba.rdf', format='xml')
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

  params = params['Categoria']
  if params["Cosmetica"] == 1 or params["Electronica"] == 1 or params["Ropa"] == 1:
    isCategorySelected = 1
  n = Namespace('http://www.owl-ontologies.com/ECSDI/projectX.owl#')
  try:
    if params["Cosmetica"] == 1 or isCategorySelected == 0:
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
    if params["Electronica"] == 1 or isCategorySelected == 0:
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
    if params["Ropa"] == 1 or isCategorySelected == 0:
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
      #No hay categoria 
  except Exception,e: 
    print str(e)
  jsondata = json.dumps(result)
  usuario = n.usuario_prueba
  nombre = Literal('Esther2')
  rdftype = n.Usuario
  g.add((usuario, RDF.type, rdftype))
  g.add((usuario,n.nombre,nombre))
  g.serialize('prueba.rdf')
  return jsondata

@app.route('/allproducts')
def all_products():
  params = request.args.get('categoria')
  g = Graph()
  try:
    g.parse('prueba.rdf', format='xml')
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
    g.parse('prueba.rdf', format='xml')
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


@app.route('/acordarProductoExterno', methods=['GET', 'POST'])
def acordarProductoExterno():
  global peticion
  if request.method == 'POST':
    peticion = json.loads(request.data)
    return "Info acuerdo recibido"
  if request.method == 'GET':
    if peticion['nombre_vendedor'] == None:
      return "No hay peticiones de vendedores externos"
    else:
      try:
        return render_template('acuerdoProductoExterno.html', params=peticion)
      except Exception, e:
        print str(e)

@app.route('/productoExternoAceptado', methods=['POST'])
def productoExternoAceptado():
  g.parse('prueba.rdf', format='xml')
  global peticion
  producto = URIRef('http://www.owl-ontologies.com/ECSDI/projectX.owl#' + str(peticion['producto']))
  categoria = URIRef('http://www.owl-ontologies.com/ECSDI/projectX.owl#' + str(peticion['categoria']))
  precio = Literal(str(peticion['precio']), datatype=XSD.integer)
  nombre_vendedor = "VendedorExterno_" + str(peticion['nombre_vendedor'])
  vendedor_externo = URIRef('http://www.owl-ontologies.com/ECSDI/projectX.owl#' + nombre_vendedor)
  try:
    g.add((producto, RDF.type, categoria))
    g.add((producto, n.precio, precio))
    g.add((producto, n.VendidoPor, vendedor_externo))
    g.add((producto, n.nombre, Literal(str(peticion['producto']))))
    g.serialize('prueba.rdf')
    return "Peticion aceptada y producto anadido al catalogo"
  except Exception, e:
    print str(e)

@app.route('/realizarPedido', methods=['POST'])
def realizarPedido():
    try:
      print 'ESTOY EN REALIZAR PEDIDO'
      '''Aqui obtengo la info del comprador'''
      info = json.loads(request.data)
      nombreComprador = "Usuario_" + info['usuario_nombre']
      print nombreComprador
      cuentaComprador = info['cuenta']
      direccionComprador = info['direccion']
      '''Aqui obtengo la Cesta'''
      Cesta = json.loads(info['Cesta'])
      '''Aqui creo el pedido'''
      g.parse('prueba.rdf', format='xml')
      global numpedido
      p = "Compra_" + str(numpedido)
      pedido = URIRef('http://www.owl-ontologies.com/ECSDI/projectX.owl#' + p)
      numeropedido = Literal(numpedido, datatype=XSD.integer)
      numpedido = numpedido + 1
      compradorDefault = URIRef('http://www.owl-ontologies.com/ECSDI/projectX.owl#' + nombreComprador)
      g.add((pedido, RDF.type, n.Compra))
      g.add((pedido, n.numeroPedido, numeropedido))
      '''Usuario de pedido por defecto'''
      g.add((pedido, n.HechoPor, compradorDefault))
      g.add((pedido, n.estadoPedido, Literal('En Proceso')))
      '''Anado productos comprados'''
      for p in Cesta:
        nprod=p['nombre']
        producto = URIRef('http://www.owl-ontologies.com/ECSDI/projectX.owl#' + nprod)
        g.add((pedido, n.Contiene, producto))
      g.serialize('prueba.rdf')
      '''LLamo al agente envios'''
      '''LLamo al agente banco'''
      return 'HECHO'
    except Exception, e:
      print str(e)

@app.route('/MisPedidos', methods=['GET'])
def mispedidos():
  try:
    result = []
    g.parse('prueba.rdf', format='xml')
    compra = URIRef('http://www.owl-ontologies.com/ECSDI/projectX.owl#' + "Compra")
    pedidos = g.triples((None, RDF.type, compra))
    for s, p, o in pedidos:
      pedidoID = s
      contieneList = []
      pedido = {'numero_pedido': '', 'usuario': '', 'estado_pedido': '','contiene': []}
      hechopor = g.triples((pedidoID, n.HechoPor, None))
      for s, p, o in hechopor:
        nombre = g.triples((o, n.nombre, None))
        for s, p, o in nombre:
          pedido['usuario'] = o.toPython()
      numero_pedido = g.triples((pedidoID, n.numeroPedido, None))
      for s, p, o in numero_pedido:
        pedido['numero_pedido'] = o.toPython()
      estado_pedido = g.triples((pedidoID, n.estadoPedido, None))
      for s, p, o in estado_pedido:
        pedido['estado_pedido'] = o.toPython()
      contiene = g.triples((pedidoID, n.Contiene, None))
      for s, p, o in contiene:
        nombre = g.triples((o, n.nombre, None))
        for s, p, o in nombre:
          producto = {'nombre': o.toPython()}
          contieneList.append(producto)
      pedido['contiene'] = json.dumps(contieneList)
      result.append(pedido)
    return json.dumps(result)
  except Exception, e:
    print str(e)

def definirNombreProducto(nombre):
  nombre_producto = ""
  for c in nombre:
    if c != " ":
      nombre_producto = nombre_producto + c
  return nombre_producto

@app.route('/Recomendaciones', methods=['GET'])
def recomendaciones():
  try:
    g.parse('prueba.rdf', format='xml')
    result = []
    productos = json.loads(request.data)
    for producto in productos:
      nombre_producto = definirNombreProducto(str(producto))
      uri = URIRef('http://www.owl-ontologies.com/ECSDI/projectX.owl#' + nombre_producto)
      print uri
      gprod = g.triples((uri, RDF.type, None))
      for s, p, o in gprod:
        prod = g.triples((None,RDF.type, o))
        for s,p,o in prod:
          nprod = g.triples((s,n.nombre,None))
          for s, p, o in nprod:
            nombre = o.toPython()
            nprec = g.triples((s,n.precio, None))
            precio = 0
            for s, p, o in nprec:
              precio = o.toPython()
              result.append({'nombre': nombre, 'precio': precio})
    return json.dumps(result)
  except Exception, e:
    print str(e)

if __name__ == '__main__':
  app.run(host='127.0.0.1', port=9001)
acuerdoVendedorExterno = {}
