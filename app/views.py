from app import app
from flask import render_template, redirect, url_for, request
from app.forms import ExtractForm
from app.models import Product

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/extract")
def extract():
    form = ExtractForm(request.form)
    if form.validate():
        product_id = form.product_id.data
        product = Product(product_id)
        if product.extract_name():
            product.extract_opinions()
            product.analyze()
            return redirect(url_for("product", product_id=product_id))
    
        return render_template("extract.html", form=form)
    return render_template("extract.html", form=form)

@app.route("/products")
def products():
    return render_template("products.html")

@app.route("/product/<product_id>")
def product(product_id):
    return render_template("product.html", product_id=product_id)

@app.route("/about")
def about():
    return render_template("about.html")