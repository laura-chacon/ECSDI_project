from flask import Flask
import requests

app = Flask(__name__)

@app.route('/busqueda')

def busqueda():
  peticion = {'categoria': 'electronica'}
  r = requests.get('http://127.0.0.1:9001/busqueda_productos', params=peticion)
  return r.text


if __name__ == '__main__':
  app.run(host='127.0.0.1', port=9000)

