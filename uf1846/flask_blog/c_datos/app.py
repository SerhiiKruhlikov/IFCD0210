# uf1846/flask_blog/c_datos/app.py
from flask import Flask, request, jsonify
import mysql.connector
import config

app = Flask(__name__)


def get_connection():
    return mysql.connector.connect(
        host=config.HOST,
        user=config.USER,
        password=config.PASSWORD,
        database=config.DATABASE,
        port=config.PORT
    )


def fetch_all(query, params=None):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query, params or ())
    result = cursor.fetchall()
    conn.close()
    return result


def fetch_one(query, params=None):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query, params or ())
    result = cursor.fetchone()
    conn.close()
    return result


def execute(query, params=None):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, params or ())
    conn.commit()
    last_id = cursor.lastrowid
    conn.close()
    return last_id


# Endpoints de usuarios


@app.route('/data/user/by-email')
def get_user_by_email():
    email = request.args.get('email')
    user = fetch_one("select * from usuarios where email = %s", (email,))
    return jsonify(user)


@app.route('/data/user', methods=['POST'])
def create_user():
    data = request.json
    user_id = execute(
        "insert into usuarios(nombre, email, pw_hash, rol, f_alta) values(%s, %s, %s, %s, %s)",
        (
            data['nombre'],
            data['email'],
            data['pw_hash'],
            data['rol'],
            data['f_alta'],
        ))
    return jsonify({'id': user_id})


# POSTS
@app.route('/data/posts')
def get_posts():
    posts = fetch_all("select * from posts")
    return jsonify(posts)


@app.route('/data/post/<int:post_id>')
def get_post_by_id(post_id):
    post = fetch_one(
        "select * from posts where id = %s",
        (post_id,)
    )
    return jsonify(post)


@app.route('/data/post', methods=['POST'])
def create_post():
    data = request.json
    post_id = execute(
        "insert into posts(titulo, contenido, estado, id_autor) values (%s, %s, %s, %s)",
        (
            data['titulo'],
            data['contenido'],
            data['estado'],
            data['id_autor'],
        )
    )
    return jsonify({'id': post_id})


@app.route('/data/post/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    data = request.json
    execute(
        "update posts set titulo=%s, contenido=%s, estado=%s where id=%s",
        (
            data['titulo'],
            data['contenido'],
            data['estado'],
            post_id,
        )
    )
    return jsonify({'id': post_id})


@app.route('/data/post/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    execute("delete from posts where id=%s", (post_id,))
    return jsonify({'id': post_id})


if __name__ == "__main__":
    app.run(port=5003, debug=True)



# curl -X POST http://127.0.0.1:5000/data/user -H "Content-Type: application/json" -d '{"nombre": "Juan Pérez", "email": "juan@example.com", "pw_hash": "hash_de_contraseña", "rol": "user", "f_alta": "2024-01-15"}'
# curl "http://127.0.0.1:5000/data/user/by-email?email=juan@example.com"

# curl -X POST http://127.0.0.1:5000/data/post -H "Content-Type: application/json" -d '{"titulo": "El post primero", "contenido": "<p>Test post</p>", "estado": "borrador", "id_autor": "1"}'
# curl -X POST http://127.0.0.1:5000/data/post/1 -H "Content-Type: application/json" -d '{"titulo": "El post primero editado", "contenido": "<p>Test post editado</p>", "estado": "publicado"}'

# curl -X POST http://127.0.0.1:5002/api/post -H "Content-Type: application/json" -d '{"titulo": "El post segundo API", "contenido": "<p>Test post de API</p>", "estado": "publicado", "id_autor": "1"}'