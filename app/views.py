from app import app

from flask import render_template

@app.route("/")
@app.route("/<name>")
def index(name="World"):
    return render_template("index.html")

@app.route("/extract")
def index(name="World"):
    return render_template("extract.html",name=name)

@app.route("/extract")
def index(name="World"):
    return render_template("extract.html",name=name)

@app.route("/product/<product_id>")
def index(name="World"):
    return render_template("product.html"product_id=product_id)

@app.route("/about")
def index(name="World"):
    return render_template("about.html")
