from flask import Flask


app = Flask(__name__)
# app.config.from_pyfile("../config.py")


from . import views

from .users.views import post_bp
app.register_blueprint(post_bp, url_prefix='/users')

from .products.views import products_bp
app.register_blueprint(products_bp, url_prefix='/products')