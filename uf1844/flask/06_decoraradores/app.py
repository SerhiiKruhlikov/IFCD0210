from flask import Flask, render_template, redirect, url_for, session, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import utilidades as util


app = Flask(__name__)
app.secret_key = "mi_clave_secreta"

USUARIOS = 'usuarios.json'


# Este es el decorador
def login_required(func):
    @wraps(func)
    def envoltura(*args, **kwargs):
        if 'id' not in session:
            flash("Por favor, inicia sesión primero")
            return redirect(url_for('login'))
        return func(*args, **kwargs)
    return envoltura


@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('principal'))
    return redirect(url_for('login'))


@app.route('/registro', methods=['GET', 'POST'])
def registrar():
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]
        if util.buscar_usuario(USUARIOS, username):
            flash(f"El usuario '{username}' ya existe")
            return redirect(url_for('registrar'))

        hashed_password = generate_password_hash(password)

        usuarios = util.cargar_datos(USUARIOS)
        user_id = len(usuarios) + 1

        usuarios.append(
            {
                "id": user_id,
                "username": username,
                "password": hashed_password
            }
        )

        util.guardar_datos(USUARIOS, usuarios)
        flash("Usuario creado correctamente")
        return redirect(url_for('login'))

    return render_template('registrar.html')


@app.route('/principal')
@login_required
def principal():
    return render_template('principal.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if 'id' in session:
        return redirect(url_for('principal'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        usuario = util.buscar_usuario(USUARIOS, username)

        if not usuario or not check_password_hash(usuario['password'], password):
            flash("Usuario o clave incorrecta")
            return redirect(url_for('login'))

        session['username'] = usuario['username']
        session['id'] = usuario['id']
        return redirect(url_for('principal'))
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    session.clear()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
