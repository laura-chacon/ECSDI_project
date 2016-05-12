from flask import Flask
import requests
from rdflib import Graph

app = Flask(__name__)

@app.route('/busqueda')

def busqueda():
  g = Graph()
  g.parse('/home2/users/alumnes/1149684/dades/linux/ECSDI/ProjectX.owl', format='xml')
  for s, p, o in g:
    print s, p, o
  peticion = {'categoria': 'electronica'}
  r = requests.get('http://127.0.0.1:9001/busqueda_productos', params=peticion)
  return r.text


if __name__ == '__main__':
  app.run(host='127.0.0.1', port=9000)

