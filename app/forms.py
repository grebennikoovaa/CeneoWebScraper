from wtforms import form, StringField, SubmitField, validators

class ExtractForm(Form):
    product_id = StringField("Product id", name="product_id", id="product_id", validators=[
        validators.DataRequired(message="Product id is required"),
        validators.length(min=6,max=10, message="Product id should have between 6 and 10 characters"),
        validators.Regexp(r'[0-9]*', message="Product id can contain only digits")

    ])
    submit = SubmitField("Extract opinions")