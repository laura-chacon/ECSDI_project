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



def existProductInCesta(nombre):
  for p in Cesta:
    if p['nombre'] == nombre:
      return True
  return False

def addProduct(nombre,cantidad,precio):
  for p in Cesta:
    if p['nombre'] == nombre:
      p['subtotal'] = cantidad*precio
      break
    
def newProduct(nombre,cantidad,precio):
  try:
    producto={"nombre": nombre, "subtotal": precio*cantidad}
    Cesta.append(producto)
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

if __name__ == '__main__':
  app.run(host='127.0.0.1', port=9000)
  
 
