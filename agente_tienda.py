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

def definirNombreProducto(nombre):
  nombre_producto = ""
  for c in nombre:
    if c != " ":
      nombre_producto = nombre_producto + c
  return nombre_producto

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
      g.parse('prueba.rdf', format='xml')
      contadorg = g.triples((n.NombrePedidos, n.contador, None))
      for s, p, o in contadorg:
          numpedido = int(o.toPython())
      '''Aqui obtengo la info del comprador'''
      info = json.loads(request.data)
      print request.data
      nombreComprador = "Usuario_" + info['usuario_nombre']
      print nombreComprador
      cuentaComprador = info['cuenta']
      direccionComprador = info['direccion']
      totalCompra = info['totalCompra']
      '''Aqui obtengo la Cesta'''
      Cesta = json.loads(info['Cesta'])
      '''Aqui creo el pedido'''
      g.parse('prueba.rdf', format='xml')
      global numpedido
      p = "Compra_" + str(numpedido)
      pedido = URIRef('http://www.owl-ontologies.com/ECSDI/projectX.owl#' + p)
      numeropedido = Literal(numpedido, datatype=XSD.integer)
      compradorDefault = URIRef('http://www.owl-ontologies.com/ECSDI/projectX.owl#' + nombreComprador)
      print 'PRUEBA AQUI'
      print Cesta
      for c in Cesta:
        print 'PRODUCTO:'
        print c
        productoUri = URIRef('http://www.owl-ontologies.com/ECSDI/projectX.owl#' + definirNombreProducto(c['nombre']))
        pProducto = str(c['subtotal'])
        precioProducto = Literal(pProducto, datatype=XSD.integer)
        if (productoUri, n.VendidoPor, None) in g:
          vendedorExt = g.triples((productoUri, n.VendidoPor, None))
          for s, p, o in vendedorExt:
            print "SUJETO"
            print s
            print "PREDICADO"
            print p
            print "OBJETO"
            print o
            nombreVendedorExterno = g.triples((o,n.nombre,None))
            nVenExt = "-"
            for s, p, o in nombreVendedorExterno:
              print o
              nVenExt = o
            cuentaVendedorExterno = g.triples((o,n.cuentaBancaria,None))
            cuentaVenExt = "-"
            for s, p, o in cuentaVendedorExterno:
              print str(o)
              cuentaVenExt = o.toPython()
            infoBancoVenExt = { "numpedido" : numpedido,
                "nombreComprador": nVenExt,
                "direccionComprador": "-",
                "totalCompra": precioProducto,
                "cuentaComprador": cuentaVenExt, 
                "tipo": "Pago Vendedor Externo"
            }
            print infoBancoVenExt
            r = requests.post('http://127.0.0.1:9003/realizarTransaccion', data=json.dumps(infoBancoVenExt))
      g.add((pedido, RDF.type, n.Compra))
      g.add((pedido, n.numeroPedido, numeropedido))
      '''Usuario de pedido por defecto'''
      g.add((pedido, n.HechoPor, compradorDefault))
      g.add((pedido, n.estadoPedido, Literal('En Proceso')))
      g.add((pedido, n.Total, Literal(totalCompra)))
      '''Anado productos comprados'''
      for p in Cesta:
            nprod = definirNombreProducto(p['nombre']) 
            producto = URIRef('http://www.owl-ontologies.com/ECSDI/projectX.owl#' + nprod)
            g.add((pedido, n.Contiene, producto))
            infoEnvio = { "numPedido" : numpedido,
                    "nombreUsuario": nombreComprador,
                    "dirreccion" : direccionComprador
                    }
            print infoEnvio
            '''r = requests.post('http://127.0.0.1:9004/derivarPedido', data=json.dumps(infoEnvio))'''
      infoBanco = { "numpedido" : numpedido,
                "nombreComprador": nombreComprador,
                "direccionComprador": direccionComprador,
                "totalCompra": totalCompra,
                "cuentaComprador": cuentaComprador, 
                "tipo": "Compra"
      }
      numpedido = numpedido + 1
      r = requests.post('http://127.0.0.1:9003/realizarTransaccion', data=json.dumps(infoBanco))
      g.set((n.NombrePedidos, n.contador, Literal(numpedido)))
      g.serialize('prueba.rdf')
      

      return 'HECHO'
    except Exception, e:
      print str(e)

@app.route('/cobroRealizado', methods=['POST'])
def cobroRealizado():
  try:
    print 'VOY A CAMBIARTE EL ESTADO PRODUCTO'
    info = json.loads(request.data)
    print info
    numPedido = info['numeroPedido']
    g.parse('prueba.rdf', format='xml')
    print info
    tipo = str(info['tipo'])
    if tipo == 'Devolucion' :
        p = "Devolucion_" + str(numPedido)
        pedido = URIRef('http://www.owl-ontologies.com/ECSDI/projectX.owl#' + p)
        print pedido
        g.set((pedido, n.estadoDevolucion, Literal('Pagado')))  
    else :
        p = "Compra_" + str(numPedido)
        pedido = URIRef('http://www.owl-ontologies.com/ECSDI/projectX.owl#' + p)
        print pedido
        g.set((pedido, n.estadoPedido, Literal('Pagado')))
    g.serialize('prueba.rdf')
    return 'OK'  
  except Exception, e:
    print str(e)
    return 'BAD'


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
        print o
        nombre = g.triples((o, n.nombre, None))
        for s, p, o in nombre:
          producto = {'nombre': o.toPython()}
          print producto
          contieneList.append(producto)
      pedido['contiene'] = json.dumps(contieneList)
      result.append(pedido)
    print result
    return json.dumps(result)
  except Exception, e:
    print str(e)

@app.route('/misDevoluciones', methods=['GET'])
def misDevoluciones():
  try:
    result = []
    g.parse('prueba.rdf', format='xml')
    devolucion = URIRef('http://www.owl-ontologies.com/ECSDI/projectX.owl#' + "Devolucion")
    devoluciones = g.triples((None, RDF.type, devolucion))
    for s, p, o in devoluciones:
      pedidoID = s
      contieneList = []
      pedido = {'numero_pedido': '', 'usuario': '', 'estado_devolucion': '','contiene': []}
      hechopor = g.triples((pedidoID, n.HechoPor, None))
      for s, p, o in hechopor:
        nombre = g.triples((o, n.nombre, None))
        for s, p, o in nombre:
          pedido['usuario'] = o.toPython()
      numero_pedido = g.triples((pedidoID, n.numeroPedido, None))
      for s, p, o in numero_pedido:
        pedido['numero_pedido'] = o.toPython()
      estado_devolucion = g.triples((pedidoID, n.estadoDevolucion, None))
      for s, p, o in estado_devolucion:
        pedido['estado_devolucion'] = o.toPython()
      contiene = g.triples((pedidoID, n.Contiene, None))
      for s, p, o in contiene:
        print o
        nombre = g.triples((o, n.nombre, None))
        for s, p, o in nombre:
          producto = {'nombre': o.toPython()}
          print producto
          contieneList.append(producto)

      pedido['contiene'] = json.dumps(contieneList)
      result.append(pedido)
    print result
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
    
@app.route('/devolverPedido')
def devolverPedido():
  try:
    g.parse('prueba.rdf', format='xml')
    result = []
    pedido = json.loads(request.data)
    numeropedido = str(pedido["numeroPedido"])
    print numeropedido
    actualPedido = URIRef('http://www.owl-ontologies.com/ECSDI/projectX.owl#Compra_' + numeropedido)
    print actualPedido
    productosList = []
    result = {"pedido": {"numeroPedido": numeropedido, "nombreUsuario": ""}, "productos": []}
    productos = g.triples((actualPedido, n.Contiene, None))
    for s, p, o in productos:
        print "entramos"
        nombreProducto = g.triples((o,n.nombre,None))
        for s,p,o in nombreProducto:
            print o
            productosList.append({'nombre': o.toPython()})
    usuario = g.triples((actualPedido, n.HechoPor, None))
    for s, p, o in usuario:
        nombreUsuario = g.triples((o, n.nombre, None))
        for s, p, o in nombreUsuario:
            result["pedido"]["nombreUsuario"] = o.toPython()
    result["productos"] = json.dumps(productosList)
    print result
    return json.dumps(result)
  except Exception, e:
    print str(e)
    
@app.route('/devolverProducto')
def devolverProducto():
  try:
    g.parse('prueba.rdf', format='xml')
    result = []
    data = json.loads(request.data)
    numeropedido = data["numeroPedido"]
    
    compra =  URIRef('http://www.owl-ontologies.com/ECSDI/projectX.owl#Compra_' + str(numeropedido))
    producto = URIRef('http://www.owl-ontologies.com/ECSDI/projectX.owl#' + definirNombreProducto((data["nombreProducto"])))
    usuario = URIRef('http://www.owl-ontologies.com/ECSDI/projectX.owl#Usuario_' + str(data["nombreUsuario"]))
    
    
    if (compra, n.Contiene, producto) in g: 
        
        print 'estamos dentro'
    
        existDev = URIRef('http://www.owl-ontologies.com/ECSDI/projectX.owl#Devolucion_' + str(numeropedido))
        
        dev = g.triples((existDev, n.numeroPedido,None))
        
        notExistDev = True
        
        for s, p, o in dev:
            devolucion = s
            g.add((devolucion, n.Contiene, Literal(str(data["nombreProducto"]))))
            g.set((devolucion, n.estadoDevolucion, Literal("Pendiente de Pago")))
            notExistDev = False
        
        if notExistDev:
            g.add((existDev, RDF.type, n.Devolucion))
            g.add((existDev, n.Contiene, producto))
	    g.add((existDev, n.numeroPedido, Literal(numeroPedido)))
            g.add((existDev, n.estadoDevolucion, Literal("Pendiente de Pago")))
            g.add((existDev, n.HechoPor, usuario))
            
        compra =  URIRef('http://www.owl-ontologies.com/ECSDI/projectX.owl#Compra_' + str(numeropedido))
        
        g.remove((compra, n.Contiene, producto))
    
        nombreUsuario = ""
        direccionComprador = ""
        totalCompra = ""
        cuentaComprador = ""
        tipo = "Devolucion"
        nombre = g.triples((usuario, n.nombre, None))
        for s, p,o in nombre:
            nombreUsuario = str(o.toPython())
        dirr = g.triples((usuario, n.direccion, None))
        for s, p,o in dirr:
            direccionComprador = str(o.toPython())
        cuent = g.triples((usuario, n.cuentaBancaria, None))
        for s, p,o in cuent:
            cuentaComprador = str(o.toPython())
        totalC = g.triples((compra, n.Total, None))
        for s, p, o in totalC:
            totalCompra = str(o.toPython())
        infoBanco = { "numpedido" : numeropedido,
                    "nombreComprador": nombreUsuario,
                    "direccionComprador": direccionComprador,
                    "totalCompra": totalCompra,
                    "cuentaComprador": cuentaComprador, 
                    "tipo": tipo
        }
    
        r = requests.post('http://127.0.0.1:9003/realizarTransaccion', data=json.dumps(infoBanco))
    
    
    
    g.serialize("prueba.rdf")
    
        
        
    return "OK"
  except Exception, e:
    print str(e)
    return "Bad"

@app.route('/obtenerValoracion')
def obtenerValoracion():
  try:
    g.parse('prueba.rdf', format='xml')
    result = []
    pedido = json.loads(request.data)
    numeropedido = str(pedido["numeroPedido"])
    nombreproducto = str(pedido["nombreProducto"]);
    print numeropedido
    compra = URIRef('http://www.owl-ontologies.com/ECSDI/projectX.owl#Compra_' + numeropedido)
    producto = URIRef('http://www.owl-ontologies.com/ECSDI/projectX.owl#' + nombreproducto)
    result = {"numeroPedido": numeropedido, "nombreProducto": nombreproducto, "nombreUsuario": "", "envio": "", "contacto": "", "estado": ""}
    valoracion = URIRef('http://www.owl-ontologies.com/ECSDI/projectX.owl#Valoracion_' + numeropedido+'_'+nombreproducto)
    if (valoracion, None, None) in g: 
        nval = g.triples((valoracion, n.comentarioEnvio, None))
        for s,p, o in nval:
            result["envio"] = o.toPython()
        nval = g.triples((valoracion, n.comentarioEstado, None))
        for s,p, o in nval:
            result["estado"] = o.toPython()
        nval = g.triples((valoracion, n.comentarioContacto, None))
        for s,p, o in nval:
            result["contacto"] = o.toPython()
        nval = g.triples((valoracion, n.HechoPor, None))
        for s, p, o in nval:
            usuario = g.triples((o, n.nombre, None))
            for s, p, o in usuario:
                result["nombreUsuario"] = o.toPython()
    else:
        g.add((valoracion, RDF.type, n.Valoracion))
	g.add((valoracion, n.Sobre, producto))
        g.add((valoracion, n.numeroPedido, Literal(numeropedido)))
        g.add((valoracion, n.comentarioEnvio, Literal("")))
        g.add((valoracion, n.comentarioEstado, Literal("")))
        g.add((valoracion, n.comentarioContacto, Literal("")))
        nval = g.triples((compra, n.HechoPor, None))
        for s, p, o in nval:
            usuario = g.triples((o, n.nombre, None))
            for s, p, o in usuario:
                result["nombreUsuario"] = o.toPython()
                uriUsuario = URIRef("http://www.owl-ontologies.com/ECSDI/projectX.owl#Usuario_"+ str(o.toPython()))
                g.add((valoracion, n.HechoPor, uriUsuario))
    g.serialize("prueba.rdf")
    return json.dumps(result)
  except Exception, e:
    print str(e)
    
@app.route('/realizarValoracion')
def realizarValoracion():
  try:
    g.parse('prueba.rdf', format='xml')
    nuevaVal = json.loads(request.data)
    numeropedido = str(nuevaVal["numeroPedido"])
    nombreproducto = str(nuevaVal["nombreProducto"])
    print numeropedido
    valoracion = URIRef('http://www.owl-ontologies.com/ECSDI/projectX.owl#Valoracion_' + numeropedido+'_'+nombreproducto)
    g.set((valoracion, n.comentarioEnvio, Literal(nuevaVal["envio"])))
    g.set((valoracion, n.comentarioEstado, Literal(nuevaVal["estado"])))
    g.set((valoracion, n.comentarioContacto, Literal(nuevaVal["contacto"])))
        
    g.serialize("prueba.rdf")
    return 'OK'
  except Exception, e:
    print str(e)
    return 'Bad'

@app.route('/pedidoEnviado',  methods=['POST'])
def pedidoEnviado():
 try:
    g.parse('prueba.rdf', format='xml')
    envio = json.loads(request.data)
    print envio
    numeroPedido = str(envio['numeroPedido'])
    pedido = URIRef('http://www.owl-ontologies.com/ECSDI/projectX.owl#Compra_' + numeroPedido)
    g.add((pedido, n.fechaEntrega, Literal(str(envio['fechaEntrega']))))
    g.add((pedido, n.EnviadoPor, Literal(envio['nombreTransportista'])))
    g.add((pedido, n.estadoEnvio, Literal("Enviado")))
    g.serialize('prueba.rdf')
    return 'OK'
 except Exception, e:
    print str(e)
    return 'Bad'


if __name__ == '__main__':
  app.run(host='127.0.0.1', port=9001)
acuerdoVendedorExterno = {}
