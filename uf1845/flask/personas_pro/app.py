import os
import uuid
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory

app = Flask(__name__)
app.secret_key = "super_secret_key"

DATABASE = "database.db"
UPLOAD_FOLDER = "fotos"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ==============================
# BASE DE DATOS
# ==============================

def get_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def crear_bd():
    conn = get_connection()
    conn.execute('''CREATE TABLE IF NOT EXISTS personas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    apellido1 TEXT NOT NULL,
    apellido2 TEXT,
    dni TEXT UNIQUE NOT NULL,
    fecha_nacimiento TEXT,
    foto TEXT)''')
    conn.commit()
    conn.close()


crear_bd()
# ==============================
# RUTAS
# ==============================

@app.route("/")
def index():
    conn = get_connection()
    personas = conn.execute("SELECT * FROM personas ORDER BY id DESC").fetchall()
    conn.close()
    return render_template("index.html", personas=personas)


@app.route("/persona/<int:id>")
def detalle(id):
    conn = get_connection()
    persona = conn.execute("SELECT * FROM personas WHERE id=?", (id,)).fetchone()
    conn.close()
    return render_template("detalle.html", persona=persona)


@app.route("/crear", methods=["GET", "POST"])
def crear():
    if request.method == "POST":

        form_data = {
            "nombre": request.form.get("nombre"),
            "apellido1": request.form.get("apellido1"),
            "apellido2": request.form.get("apellido2"),
            "dni": request.form.get("dni"),
            "fecha_nacimiento": request.form.get("fecha_nacimiento"),
            "foto": None
        }

        foto = request.files["foto"]
        filename = None

        if foto and foto.filename:
            if not allowed_file(foto.filename):
                flash("Formato de imagen no permitido.", "danger")
                return render_template("form.html", persona=form_data)

            ext = os.path.splitext(foto.filename)[1]
            filename = f"{uuid.uuid4()}{ext}"
            foto.save(os.path.join(UPLOAD_FOLDER, filename))

        try:
            conn = get_connection()
            conn.execute("""
                INSERT INTO personas
                (nombre, apellido1, apellido2, dni, fecha_nacimiento, foto)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (form_data["nombre"],
                form_data["apellido1"],
                form_data["apellido2"],
                form_data["dni"],
                form_data["fecha_nacimiento"],
                filename))
            conn.commit()
            conn.close()

            flash("Persona creada correctamente.", "success")
            return redirect(url_for("index"))

        except sqlite3.IntegrityError:
            flash("El DNI ya existe.", "danger")
            return render_template("form.html", persona=form_data)

    return render_template("form.html", persona=None)


@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):

    conn = get_connection()
    persona = conn.execute("SELECT * FROM personas WHERE id=?", (id,)).fetchone()

    if request.method == "POST":

        form_data = {
            "id": id,
            "nombre": request.form.get("nombre"),
            "apellido1": request.form.get("apellido1"),
            "apellido2": request.form.get("apellido2"),
            "dni": request.form.get("dni"),
            "fecha_nacimiento": request.form.get("fecha_nacimiento"),
            "foto": persona["foto"]
        }

        filename = persona["foto"]
        nueva_foto = request.files["foto"]

        if nueva_foto and nueva_foto.filename:
            if not allowed_file(nueva_foto.filename):
                flash("Formato de imagen no permitido.", "danger")
                conn.close()
                return render_template("form.html", persona=form_data)

            ext = os.path.splitext(nueva_foto.filename)[1]
            filename = f"{uuid.uuid4()}{ext}"
            nueva_foto.save(os.path.join(UPLOAD_FOLDER, filename))

            if persona["foto"]:
                try:
                    os.remove(os.path.join(UPLOAD_FOLDER, persona["foto"]))
                except:
                    pass

        try:
            conn.execute("""
                UPDATE personas
                SET nombre=?, apellido1=?, apellido2=?, 
                    dni=?, fecha_nacimiento=?, foto=?
                WHERE id=?
            """, (form_data["nombre"],
                  form_data["apellido1"],
                  form_data["apellido2"],
                  form_data["dni"],
                  form_data["fecha_nacimiento"],
                  filename,
                  id))

            conn.commit()
            conn.close()

            flash("Persona actualizada correctamente.", "success")
            return redirect(url_for("detalle", id=id))

        except sqlite3.IntegrityError:
            flash("El DNI ya existe.", "danger")
            conn.close()
            return render_template("form.html", persona=form_data)

    conn.close()
    return render_template("form.html", persona=persona)


@app.route("/eliminar/<int:id>")
def eliminar(id):
    conn = get_connection()
    persona = conn.execute("SELECT foto FROM personas WHERE id=?", (id,)).fetchone()

    if persona["foto"]:
        try:
            os.remove(os.path.join(UPLOAD_FOLDER, persona["foto"]))
        except:
            pass

    conn.execute("DELETE FROM personas WHERE id=?", (id,))
    conn.commit()
    conn.close()

    flash("Persona eliminada correctamente.", "success")
    return redirect(url_for("index"))


@app.route("/fotos/<filename>")
def fotos(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


if __name__ == "__main__":
    app.run(debug=True)