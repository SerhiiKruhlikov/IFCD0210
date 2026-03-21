import requests
from pprint import pprint


url = "http://127.0.0.1:5000/usuarios/1"
respuesta = requests.get(url)
pprint(respuesta.json())
