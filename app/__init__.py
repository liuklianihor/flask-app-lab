from flask import Flask, render_template
from datetime import timedelta 
from . import views
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .config import config_map
from sqlalchemy.orm import DeclarativeBase
import os
from sqlalchemy import MetaData

from dotenv import load_dotenv
load_dotenv()

class Base(DeclarativeBase):
    metadata = MetaData(naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
    })

db = SQLAlchemy(model_class=Base)
migrate = Migrate()

def create_app(config_name: str = os.environ.get("FLASK_CONFIG", "dev")) -> Flask:
    app = Flask(__name__)
    app.secret_key = "my-secret-key"
    app.config.from_object(config_map[config_name])
    # app.config.from_pyfile("../config.py")
    app.permanent_session_lifetime = timedelta(seconds=120)

    print(f"Running in config: {config_name}")


    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context(): 
        from .users import models
        from .posts import models

        from .views import main as main_blueprint
        app.register_blueprint(main_blueprint, url_prefix='/main')

        from .users.views import users_bp
        app.register_blueprint(users_bp, url_prefix='/users')

        from .products.views import products_bp
        app.register_blueprint(products_bp, url_prefix='/products')

        from .auth.views import auth_bp
        app.register_blueprint(auth_bp, url_prefix="/auth")

        from .posts.views import post_bp
        app.register_blueprint(post_bp, url_prefix="/posts")

        #if config_name == "test":
        #    print("Registered routes:")
        #    for rule in app.url_map.iter_rules():
        #        print(rule)

    @app.errorhandler(404)
    def not_found(e):
        return render_template('404.html'), 404
     
    return app