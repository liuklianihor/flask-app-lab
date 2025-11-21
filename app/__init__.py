from flask import Flask
from datetime import timedelta 

app = Flask(__name__)
app.secret_key = "my-secret-key"
# app.config.from_pyfile("../config.py")

app.permanent_session_lifetime = timedelta(seconds=30)

from . import views

from .users.views import post_bp
app.register_blueprint(post_bp, url_prefix='/users')

from .products.views import products_bp
app.register_blueprint(products_bp, url_prefix='/products')

from .auth.views import auth_bp
app.register_blueprint(auth_bp, url_prefix="/auth")