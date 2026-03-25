# uf1846/flask_blog/c_negocio/app.py
import requests
from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

RUTA_DATOS = 'http://localhost:5003/data'


def get_user_by_email(email):
    resp = requests.get(f"{RUTA_DATOS}/user/by-email", params={'email': email})
    return resp.json()


def create_user(data):
    resp = requests.post(f"{RUTA_DATOS}/user", json=data)
    return resp.json()


def get_posts_db():
    resp = requests.get(f"{RUTA_DATOS}/posts")
    return resp.json()


def get_post_db(post_id):
    resp = requests.get(f"{RUTA_DATOS}/post/{post_id}")
    return resp.json()


def create_post_db(data):
    resp = requests.post(f"{RUTA_DATOS}/post", json=data)
    return resp.json()


def update_post_db(post_id, data):
    resp = requests.put(f"{RUTA_DATOS}/post/{post_id}", json=data)
    return resp.json()


def delete_post_db(post_id):
    resp = requests.delete(f"{RUTA_DATOS}/post/{post_id}")
    return resp.json()


def validar_post(data):
    required = [
        'titulo',
        'contenido',
        'estado',
        # 'id_autor',
    ]

    for campo in required:
        if not campo in data:
            return False

    return True


@app.route("/api/login", methods=['POST'])
def login():
    data = request.json
    user = get_user_by_email(data['email'])

    if not user:
        return jsonify({'error': 'El usuario no existe.'}), 401

    if not check_password_hash(user['pw_hash'], data['password']):
        return jsonify({'error': 'El password incorrecta.'}), 401

    return jsonify(
        {
            'mensaje': 'Login correcto',
            'user_id': user['id'],
            'rol': user['rol']
        }
    )


@app.route("/api/posts")
def get_posts():
    posts = get_posts_db()
    publicados = []

    for p in posts:
        if p['estado'] == 'publicado':
            publicados.append(p)

    return jsonify(publicados)


@app.route("/api/posts_all")
def get_posts_all():
    posts = get_posts_db()
    return jsonify(posts)


@app.route("/api/posts/<int:post_id>")
def get_post(post_id):
    post = get_post_db(post_id)

    # if not post or post['estado'] != 'publicado':
    #     return jsonify({'error': 'No encontrado'}), 404

    return jsonify(post)


@app.route("/api/post", methods=['POST'])
def create_post():
    data = request.json

    if validar_post(data):
        post = {
            'titulo': data['titulo'],
            'contenido': data['contenido'],
            'estado': data['estado'],
            # 'id_autor': data['id_autor'],
        }
        resultado = create_post_db(post)
        return jsonify(resultado)

    return jsonify({'error': 'Faltan campos obligatorios'}), 400


@app.route('/api/post/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    data = request.json
    if validar_post(data):
        update_post_db(post_id, data)
        return jsonify({'mensaje': 'Post actualizado'})

    return jsonify({'error': 'Faltan campos obligatorios'}), 400


@app.route('/api/post/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    delete_post_db(post_id)
    return jsonify({'mensaje': 'Post eliminado'})


if __name__ == "__main__":
    app.run(port=5002, debug=True)
