from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_minify import minify
from .config import Config
# Adding API functionality
from flask_restful import Api
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
api = Api()
ma = Marshmallow()


def create_app(config_class=Config, api=api, ma=ma, db=db):
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initializing API routes
    from flaskapp.api.routes import initialize_api_routes
    initialize_api_routes(api)

    # Initiating app components
    db.init_app(app)
    api.init_app(app)
    ma.init_app(app)

    Migrate(app, db)

    from flaskapp.main.routes import main
    from flaskapp.errors.handlers import errors
    from flaskapp.api.routes import api_bp

    app.register_blueprint(main)
    app.register_blueprint(errors)
    app.register_blueprint(api_bp)

    minify(app)

    return app


app = create_app()
