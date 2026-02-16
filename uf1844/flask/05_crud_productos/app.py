from flask import Flask, render_template, request, url_for, redirect
from datetime import datetime
import json
import os

app = Flask(__name__)

PRODUCTOS = "productos.json"


def carga(archivo):
    with open(archivo, "r", encoding="utf-8") as f:
        return json.load(f)


def guardar(archivo, datos):
    with open(archivo, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)


def new_id(archivo):
    datos = carga(archivo)
    result = max([p.get("id", 0) for p in datos['products']], default=0) + 1
    return result


@app.route("/")
def index():
    datos = carga(PRODUCTOS)

    categories = datos["categories"]
    products = datos["products"]

    current_product = None
    product_id = request.args.get("products")

    if product_id is not None and product_id != "-1":
        product_id = int(product_id)
        for product in products:
            if product["id"] == product_id:
                current_product = product
                break

    context = {
        "categories": categories,
        "products": products,
        "current_product": current_product,
    }

    return render_template('index.html', **context)


@app.route("/update/<int:product_id>", methods=["POST"])
def update(product_id):
    datos = carga(PRODUCTOS)

    categories = datos["categories"]
    products = datos["products"]

    current_product = None

    for product in datos["products"]:
        if product["id"] == product_id:
            current_product = product
            break

    if current_product:
        current_product["name"] = request.form["name"]
        current_product["price"] = float(request.form["price"])
        current_product["category_id"] = int(request.form["category"])

    guardar(PRODUCTOS, datos)

    context = {
        "categories": categories,
        "products": products,
        "current_product": current_product,
    }

    return redirect(url_for("index", products=current_product["id"]))


@app.route("/create", methods=["POST"])
def create():
    datos = carga(PRODUCTOS)

    categories = datos["categories"]
    products = datos["products"]

    product = {
        "id": new_id(PRODUCTOS),
        "name": request.form["name"],
        "price": float(request.form["price"]),
        "category_id": int(request.form['category'])
    }

    products.append(product)
    guardar(PRODUCTOS, datos)

    return redirect(url_for("index", products=product["id"]))


@app.route("/delete/<int:product_id>")
def delete(product_id):
    datos = carga(PRODUCTOS)

    datos["products"] = [p for p in datos["products"] if p["id"] != product_id]

    guardar(PRODUCTOS, datos)

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
