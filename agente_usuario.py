from flask import Flask, render_template, request, url_for
import requests
from rdflib import Graph
from rdflib import URIRef, BNode, Literal, Namespace, RDF
from rdflib.namespace import FOAF
from rdflib.namespace import XSD
import rdflib

app = Flask(__name__)

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
  print r
  return str(r.content)

@app.route('/getCategory', methods=['POST'])
def getCategory():
  try:
    if ('Electronica' in request.form):
      peticion = {'categoria': 'Electronica'}
      r = requests.get('http://127.0.0.1:9001/busqueda_productos', params=peticion)
      return str(r.content)
    elif ('Ropa' in request.form):
      peticion = {'categoria': 'Ropa'}
      r = requests.get('http://127.0.0.1:9001/busqueda_productos', params=peticion)
      return str(r.content)
    elif ('Cosmetica' in request.form):
      peticion = {'categoria': 'Cosmetica'}
      r = requests.get('http://127.0.0.1:9001/busqueda_productos', params=peticion)
      return str(r.content)
    return 'OK'
  except Exception,e:
    print str(e)
    return 'Bad'

if __name__ == '__main__':
  app.run(host='127.0.0.1', port=9000)
