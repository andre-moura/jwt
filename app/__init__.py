from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    # Import models here to ensure they are registered with SQLAlchemy
    from app.models import User

    # Register blueprints/routes here
    from app.routes.auth import auth
    from app.routes.protected import protected
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(protected, url_prefix='/protected')

    return app