from flask import Flask, render_template, request, url_for, redirect
from datetime import datetime
import json
import os

app = Flask(__name__)

DATOS = "datos.json"

PAISES = ["Argentina", "Mexico", "Espana", ]
GENEROS = ["Hombre", "Mujer", "No definido", ]
HOBBIES = ["Leer", "Deporte", "Musica", "Video juegos", "Viajar", ]


@app.route("/", methods=["POST", "GET"])
def index():
    datos = {}

    if request.method == "POST":

        datos = {
            "pais": request.form.get("pais"),
            "genero": request.form.get("genero"),
            "hobbies": request.form.getlist("hobbies"),
        }

        with open(DATOS, "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=4, ensure_ascii=False)


    # Leer del archivo
    # with open(DATOS, "r", encoding="utf-8") as f:
    #     datos = json.load(f)

    context = {
        "paises": PAISES,
        "generos": GENEROS,
        "hobbies": HOBBIES,
        "datos": {},
    }

    return render_template('index.html', **context)


@app.route("/carga")
def carga():
    with open(DATOS, "r", encoding="utf-8") as f:
        datos = json.load(f)

    context = {
        "paises": PAISES,
        "generos": GENEROS,
        "hobbies": HOBBIES,
        "datos": datos,
    }

    return render_template("index.html", **context)


if __name__ == "__main__":
    app.run(debug=True)
