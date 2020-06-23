from flask import Flask


from src.blueprints.auth import bp as auth_bp
from src.blueprints.users import bp as users_bp
from src.blueprints.categories import bp as categories_bp
from src.blueprints.operations import bp as operations_bp
from src.database import db


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(users_bp, url_prefix='/users')
    app.register_blueprint(categories_bp, url_prefix='/categories')
    app.register_blueprint(operations_bp, url_prefix='/operations')
    db.init_app(app)
    return app

