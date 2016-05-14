from flask import Flask
import requests
from rdflib import Graph
from rdflib import URIRef, BNode, Literal, Namespace, RDF

app = Flask(__name__)

@app.route('/busqueda')

def busqueda():
  g = Graph()
  n = Namespace('http://www.owl-ontologies.com/ECSDI/projectX.owl')
  g.parse('basededatos1.owl', format='xml')
  result = g.query(
    """PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
       PREFIX usuario: <http://www.owl-ontologies.com/ECSDI/projectX.owl#>
       SELECT ?user
        WHERE { ?user usuario:nombre ? "Esther"
      }
  """)
  print('resultados')
  for s,p,o in result: 
    print o
  peticion = {'categoria': 'electronica'}
  r = requests.get('http://127.0.0.1:9001/busqueda_productos', params=peticion)
  return r.text


if __name__ == '__main__':
  app.run(host='127.0.0.1', port=9000)

