# uf1846/flask_blog/c_front/app.py
from flask import Flask, render_template, abort, request, session, redirect, flash
import requests


app = Flask(__name__)
app.secret_key = "supersecreto"


API = "http://negocio:5002/api"


def get_posts():
    return requests.get(f"{API}/posts").json()


def get_posts_all():
    return requests.get(f"{API}/posts_all").json()


def get_post(post_id):
    response = requests.get(f"{API}/posts/{post_id}")

    if response.status_code == 404:
        return None

    return response.json()


def is_admin():
    return session.get('rol') == 'admin'


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


@app.route('/')
def index():
    posts = get_posts()
    context = {
        'posts': posts,
    }
    return render_template('home.html', **context)


@app.route('/posts/<int:post_id>')
def get_post_by_id(post_id):
    post = get_post(post_id)

    if post is None:
        abort(404)

    context = {
        'post': post,
    }
    return render_template('post.html', **context)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        data = {
            'email': request.form['email'],
            'password': request.form['password'],
        }
        response = requests.post(f"{API}/login", json=data)

        if response.status_code == 200:
            user = response.json()
            session['user_id'] = user['user_id']
            session['rol'] = user['rol']
            return redirect('/admin')
        else:
            flash('Credenciales incorrectas.')

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


@app.route('/admin')
def admin():
    if not is_admin():
        return redirect('/login')

    posts = get_posts_all()
    return render_template('admin.html', posts=posts)


@app.route('/admin/create', methods=['POST', 'GET'])
def create_post():
    if not is_admin():
        return redirect('/login')

    if request.method == 'POST':
        data = {
            'titulo': request.form['titulo'],
            'contenido': request.form['contenido'],
            # 'id_author': session.get('user_id'),
            'estado': request.form['estado']
        }

        requests.post(f"{API}/post", json=data)
        flash('Post creado con éxito.')
        return redirect('/admin')

    return render_template('create_post.html', post=None)


@app.route('/admin/edit/<int:post_id>', methods=['POST', 'GET'])
def edit_post(post_id):
    if not is_admin():
        return redirect('/login')

    if request.method == 'PUT':
        data = {
            'titulo': request.form['titulo'],
            'contenido': request.form['contenido'],
            'estado': request.form['estado']
        }

        requests.post(f"{API}/post/{post_id}", json=data)
        flash('Post actualizado con éxito.')
        return redirect('/admin')

    context = {
        'post': get_post(post_id)
    }
    return render_template('create_post.html', **context)


@app.route('/admin/delete/<int:post_id>')
def delete_post(post_id):
    if not is_admin():
        return redirect('/login')

    requests.delete(f"{API}/post/{post_id}")
    flash('Post eliminado con éxito.')
    return redirect('/admin')



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
