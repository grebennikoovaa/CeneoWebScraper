from app import app
from flask import render_template, redirect, url_for, request
from app.forms import ExtractForm
from app.models import Product

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/extract")
def render_form():
    form = ExtractForm()
    return render_template("extract.html", form=form)

@app.route("/extract", methods=['POST'])
def extract():
    form = ExtractForm(request.form)
    if form.validate():
        product_id = form.product_id.data
        product = Product(product_id)
        if product.extract_name():
            product.extract_opinions()
            product.analyze()
            product.export_info()
            product.export_opinions()
            return redirect(url_for('product', product_id=product_id))
        form.product_id.errors.append('There is no product for provided id or product has no opinions')
        return render_template('extract.html', form=form)
    return render_template('extract.html', form=form)

@app.route("/products")
def products():
    products_data = []
    directory = "./app/data/products"

    for filename in os.listdir(directory):
        if filename.endswith("_info.json"):
            with open(os.path.join(directory, filename), encoding="utf-8") as f:
                data = json.load(f)
                stats = data["stats"]
                products_data.append({
                    "product_id": data["product_id"],
                    "product_name": data["product_name"],
                    "opinions_count": stats["opinions_count"],
                    "pros_count": stats["pros_count"],
                    "cons_count": stats["cons_count"],
                    "average_score": stats["average_rate"]
                })

    return render_template("products.html", products=products_data)

@app.route("/product/<product_id>")
def product(product_id):
    try:
        with open(f"./app/data/products/{product_id}_info.json", encoding="utf-8") as f:
            product = json.load(f)
        return render_template("product.html", product=product)
    except:
        return "Product not found", 404

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/download/<product_id>/<format>")
def download_opinions(product_id, format):
    from app.models import Product
    import pandas as pd
    from io import BytesIO
    from flask import send_file

    product = Product(product_id)
    product.import_opinions()
    df = pd.DataFrame([op.transform_to_dict() for op in product.opinions])

    if format == "csv":
        return send_file(BytesIO(df.to_csv(index=False).encode("utf-8")),
                         download_name=f"{product_id}.csv", as_attachment=True)
    elif format == "xlsx":
        output = BytesIO()
        df.to_excel(output, index=False)
        output.seek(0)
        return send_file(output, download_name=f"{product_id}.xlsx", as_attachment=True)
    elif format == "json":
        return send_file(BytesIO(df.to_json(orient="records", force_ascii=False).encode("utf-8")),
                         download_name=f"{product_id}.json", as_attachment=True)
    return "Unsupported format", 400