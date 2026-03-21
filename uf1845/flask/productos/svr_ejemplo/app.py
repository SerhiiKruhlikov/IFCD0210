from flask import Flask, jsonify


app = Flask(__name__)


usuarios = {
    1: {
        "nombre": "Paco",
        "edad": "44"
    },
    2: {
        "nombre": "Ana",
        "edad": "22"
    }
}

@app.route("/usuarios/<int:id>")
def obtener_usr(id):
    usuario = usuarios.get(id)
    return jsonify(usuario)


if __name__ == "__main__":
    app.run(debug=True)
