from flask import Flask, request

app = Flask(__name__)

@app.route('/busqueda_productos')

def busqueda_productos():
  
  params = request.args.get('categoria')
  
  print params
  return "chupis"

if __name__ == '__main__':
  app.run(host='127.0.0.1', port=9001)