from flask import Flask, jsonify, render_template, request, url_for
import requests
import json
from rdflib import Graph
from rdflib import URIRef, BNode, Literal, Namespace, RDF
from rdflib.namespace import FOAF
from rdflib.namespace import XSD
import rdflib

app = Flask(__name__)


Cesta = []

g = Graph()
n = Namespace('http://www.owl-ontologies.com/ECSDI/projectX.owl#')

def existProductInCesta(nombre):
  for p in Cesta:
    if p['nombre'] == nombre:
      return True
  return False

def addProduct(nombre,precio,cantidad):
  for p in Cesta:
    if p['nombre'] == nombre:
      p['cantidad'] == cantidad;
      p['subtotal'] = cantidad*precio
      break

def getTotalCesta():
  total = 0
  for p in Cesta:
    print 'voy a sumar'
    print str(total)
    print p['subtotal']
    total = total + p['subtotal']
  return total 
    
def newProduct(nombre,precio,cantidad):
  try:
    producto={"nombre": nombre, "cantidad":cantidad,"subtotal": precio*cantidad}
    Cesta.append(producto)
  except Exception,e:
    print e
  
def deleteProduct(nombre,cantidad,subtotal):
  try:
    producto={"nombre": nombre, "cantidad":cantidad,"subtotal": subtotal}
    Cesta.remove(producto)
    print Cesta
  except Exception,e:
    print e      

@app.route('/busqueda')

def busqueda():
  try:
    return render_template('busquedaPage.html')
  except Exception,e:
    print str(e)
    return 'Bad'

  """try:
    input_var = raw_input("Enter something: ")
    print str("you entered " + input_var) 
  except Exception, e:
    print str(e)
  peticion = {'categoria': 'Cosmetica'}
  r = requests.get('http://127.0.0.1:9001/busqueda_productos', params=peticion)
  print r
  return str(r.content)"""

@app.route('/catalog')

def catalog():
  r = requests.get('http://127.0.0.1:9001/allproducts')
  return render_template('listofproducts.html', products=json.loads(r.content))

@app.route('/getCategory', methods=['POST'])
def getCategory():
  peticion = {}
  filtroSeleccionado = 0
  peticion = {"Categoria": {"Ropa": 0, "Electronica": 0, "Cosmetica": 0}, "Precio": {"De0a30": 0, "De30A100": 0, "MayorA100": 0}}
  try:
    if ('Electronica' in request.form):
      filtroSeleccionado = 1
      peticion["Categoria"]["Electronica"] = 1
    if ('Ropa' in request.form):
      peticion["Categoria"]["Ropa"] = 1
      filtroSeleccionado = 1
    if ('Cosmetica' in request.form):      
      peticion["Categoria"]["Cosmetica"] = 1
      filtroSeleccionado = 1
    if ('De0a30' in request.form):
      peticion["Precio"]["De0a30"] = 1
      filtroSeleccionado = 1
    if ('De30A100' in request.form):
      peticion["Precio"]["De30A100"] = 1
      filtroSeleccionado = 1
    if ('MayorA100' in request.form):      
      peticion["Precio"]["MayorA100"] = 1
      filtroSeleccionado = 1
    if filtroSeleccionado == 1: 
      jsondata = json.dumps(peticion)
      r = requests.get('http://127.0.0.1:9001/busqueda_productos', data=jsondata)
    else:
      r = requests.get('http://127.0.0.1:9001/allproducts')
    return render_template('listofproducts.html', products=json.loads(r.content))
  except Exception,e:
    print str(e)
    return 'Bad'

@app.route('/pedidos')

def pedidos():
  r = requests.get('http://127.0.0.1:9001/pedidos')
  return r.content

@app.route('/Cesta')
def printCesta():
  try:
    result = []
    g.parse('prueba.rdf', format='xml')
    allUsers = g.triples((None, RDF.type, n.Usuario))
    for s,p,o in allUsers:
      nombre_user = g.triples((s, n.nombre, None))
      for s,p,o in nombre_user:
        nombre = o.toPython()
        cuenta = g.value(s, n.cuentaBancaria)
        direccion = g.value(s, n.direccion)
        result.append({'nombre': nombre, 'cuentaBancaria': cuenta, 'direccion': direccion})
    totalprecio = getTotalCesta()  
    print totalprecio
    return render_template('cesta.html', productos=Cesta , dusers=result, total=totalprecio)
  except Exception, e:
    print str(e)
    return 'Bad'

@app.route('/addProductCesta')
def  addProductCesta():
  
  try:
    nombre = request.args.get("nombre")
    precio = request.args.get("precio", 0, type=int)
    cantidad = request.args.get("cantidad", 0, type=int)
    if existProductInCesta(nombre):
      addProduct(nombre,precio,cantidad)
    else :
      newProduct(nombre,precio,cantidad)
      
  except Exception, e:
    print str(e)
    return 'Bad'
  return 'OK'

@app.route('/deleteProductCesta')
def  deleteProductCesta():
  print 'hola que taaaaaal'
  try:
    nombre = request.args.get("nombre")
    cantidad = request.args.get("cantidad", 0, type=int)
    subtotal = request.args.get("subtotal", 0, type=int)
    if existProductInCesta(nombre):
      deleteProduct(nombre,cantidad,subtotal)
      print 'El producto' + nombre + 'se va a eliminar'
    else :
      return 'This product doesnt exist'
      
  except Exception, e:
    print str(e)
    return 'Bad'
  return 'OK'


@app.route('/realizarPedido', methods=['POST'])
def  realizarPedido():
  try:
    print 'La cesta voy a hacerla en json'
    '''print json.loads(Cesta)'''
    usuario = request.form["nombres_usuarios"]
    cuenta = request.form["cuentas"]
    direc = request.form["direcciones"]
    total = getTotalCesta()
    infocomprador = {"usuario_nombre": usuario,
                    "cuenta": cuenta,
                    "direccion": direc,
                    "Cesta": json.dumps(Cesta),
                    "totalCompra": total
        }
    r = requests.post('http://127.0.0.1:9001/realizarPedido', data=json.dumps(infocomprador))      
  except Exception, e:
    print str(e)
    return 'Bad'
  return 'OK'

@app.route('/MisPedidos')
def mispedidos():
  try:
    r = requests.get('http://127.0.0.1:9001/MisPedidos')
    pedidos = json.loads(r.content)
    return render_template('mispedidos.html', pedidos=pedidos)
  except Exception, e:
    print str(e)


@app.route('/Recomendaciones')
def recomendaciones():
  try:
    infoCesta = []
    for product in Cesta:
      infoCesta.append(product['nombre'])
    r = requests.get('http://127.0.0.1:9001/Recomendaciones', data=json.dumps(infoCesta))
    recomendaciones = json.loads(r.content)
    return render_template('recomendaciones.html', recomendaciones=recomendaciones)
  except Exception, e:
    print str(e)

if __name__ == '__main__':
  app.run(host='127.0.0.1', port=9000)
