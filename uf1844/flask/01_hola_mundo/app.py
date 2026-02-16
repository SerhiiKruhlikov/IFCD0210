from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def index():
    return "Hola mundo"


@app.route("/about")
def about():
    cadena = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>

    <h1>Hola Usuario</h1>
    <h2>Bienvenido a mi sitio Flask</h2>

</body>
</html>"""
    return cadena


@app.route("/prueba")
def prueba():
    return render_template('prueba.html')


@app.route("/prueba/<string:nombre>")
@app.route("/prueba/<string:nombre>/<int:numero>")
def saludo(nombre):
    return render_template('prueba.html', nombre=nombre)


@app.route("/suma", methods=["GET", "POST"])
def suma():
    if request.method == "POST":
        num1 = request.form["num1"]
        num2 = request.form["num2"]
        return str(int(num1) + int(num2))
    else:
        cadena = """
        <form action='/suma' method='post'>
            <input name='num1' type='text' />
            <input name='num2' type='text' />
            <input type='submit' value='submit' />
        </form>
        """
    return cadena


@app.route("/jinja")
def jinja():
    context = {
        'nombre': 'Serhii',
        'apellido': 'Kruhlikov',
        'numeros': ['unos', 'dos', 'tres', 'cuatro',],
    }
    return render_template('jinja.html', **context)


if __name__ == "__main__":
    app.run(debug=True)
