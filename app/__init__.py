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
    from app.routes.auth import auth_bp
    app.register_blueprint(auth_bp)

    return app