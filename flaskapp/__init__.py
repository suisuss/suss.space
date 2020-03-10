from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_minify import minify
from .config import Config

db = SQLAlchemy()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    Migrate(app, db)

    from flaskapp.main.routes import main
    from flaskapp.errors.handlers import errors

    app.register_blueprint(main)
    app.register_blueprint(errors)

    minify(app)

    return app


app = create_app()
