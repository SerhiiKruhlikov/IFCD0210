from flask import Flask, render_template, request, url_for, redirect
from datetime import datetime
import json
import os

app = Flask(__name__)
MIS_TAREAS = "tareas.json"


def carga_tareas():
    if not os.path.exists(MIS_TAREAS):
        return []
    with open(MIS_TAREAS, "r", encoding="utf-8") as f:
        return json.load(f)


def guardar_tareas(tareas):
    with open(MIS_TAREAS, "w", encoding="utf-8") as f:
        json.dump(tareas, f, indent=4, ensure_ascii=False)


@app.route("/", methods=["POST", "GET"])
def index():
    tareas = carga_tareas()

    if request.method == "POST":

        if not request.form["description"].strip():
            return redirect(url_for("index"))

        nuevo_id = max([t.get("id", 0) for t in tareas], default=0) + 1

        nueva = {
            "id": nuevo_id,
            "description": request.form["description"].strip(),
            "fecha_alta": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "fecha_completa": None
        }

        tareas.append(nueva)
        guardar_tareas(tareas)
        return redirect(url_for("index"))

    return render_template('index.html', tareas=tareas)


@app.route('/delete/<int:id_tarea>', methods=["POST", "GET"])
def borrar_tarea(id_tarea):
    tasks = carga_tareas()
    resto_tareas = []

    for t in tasks:
        if t['id'] != id_tarea:
            resto_tareas.append(t)

    guardar_tareas(resto_tareas)
    return redirect(url_for("index"))


@app.route('/completar/<int:id_tarea>', methods=["POST", "GET"])
def completar_tarea(id_tarea):
    tasks = carga_tareas()

    for t in tasks:
        if t['id'] == id_tarea:
            t['fecha_completa'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            break

    guardar_tareas(tasks)
    return redirect(url_for("index"))


@app.route("/cambiar/<int:id_tarea>", methods=["POST", "GET"])
def cambiar_tarea(id_tarea):
    tasks = carga_tareas()
    tarea_sel = ""

    for t in tasks:
        if t['id'] == id_tarea:
            tarea_sel = t
            break

    if request.method == "POST":
        tarea_sel["description"] = request.form["description"].strip()
        tarea_sel["fecha_completa"] = None

        guardar_tareas(tasks)
        return redirect(url_for("index"))

    return render_template('edit.html', tarea=tarea_sel)


if __name__ == "__main__":
    app.run(debug=True)
