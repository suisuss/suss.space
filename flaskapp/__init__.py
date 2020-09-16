from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_minify import minify
from .config import Config
from flask_restful import Api
from flask_marshmallow import Marshmallow
from flask_praetorian import Praetorian
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
db = SQLAlchemy()
bcrypt = Bcrypt()
api = Api()
ma = Marshmallow()
guard = Praetorian()


login_manager = LoginManager()
login_manager.login_view = 'admin.adminn'
login_manager.login_message_category = 'info'


def create_app(config_class=Config, api=api, ma=ma, db=db):
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initializing API routes
    from flaskapp.api.routes import initialise_api_routes
    initialise_api_routes(api)

    # Initiating app components
    from flaskapp.admin.models import User
    guard.init_app(app, User)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    api.init_app(app)
    ma.init_app(app)


    Migrate(app, db)

    from flaskapp.main.routes import main
    from flaskapp.admin.routes import admin
    from flaskapp.errors.handlers import errors
    from flaskapp.api.routes import api_bp

    app.register_blueprint(main)
    app.register_blueprint(admin)
    app.register_blueprint(errors)
    app.register_blueprint(api_bp)

    minify(app)

    return app


app = create_app()
