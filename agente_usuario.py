from flask import Flask
import requests
from rdflib import Graph
from rdflib import URIRef, BNode, Literal, Namespace, RDF

app = Flask(__name__)

@app.route('/busqueda')

def busqueda():
  g = Graph()
  print ('antes del load')
  g.load('basededatos1.owl', format='xml')
  print ('hemos cargado el grafo')
  try:
    result = g.query(
      """PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
	SELECT ?nombre
	  WHERE { 
	  ?user usuario:nombre ?nombre.
	  FILTER( str(?nombre) = "Esther").
	  }
    """, initNs = dict(usuario="http://www.owl-ontologies.com/ECSDI/projectX.owl#"))
    print('resultados')
    for row in result.result: 
      print row
  except Exception,e: 
    print str(e)
  peticion = {'categoria': 'electronica'}
  r = requests.get('http://127.0.0.1:9001/busqueda_productos', params=peticion)
  return r.text


if __name__ == '__main__':
  app.run(host='127.0.0.1', port=9000)

