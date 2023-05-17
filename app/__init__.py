from flask import Flask
from flask_pymongo import PyMongo
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from .auth.routes import auth as auth_blueprint
from .main.routes import main as main_blueprint
from .config import Config
from .models import User

mongo = PyMongo()
bcrypt = Bcrypt()
login_manager = LoginManager()
jwt = JWTManager()
login_manager.login_view = 'auth.login'


def init_login_manager(app):
    @login_manager.user_loader
    def load_user(username):
        return User(username)


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    print(app.config["SECRET_KEY"])

    mongo.init_app(app)
    bcrypt.init_app(app)
    app.db = mongo.db
    login_manager.init_app(app)
    jwt.init_app(app)

    init_login_manager(app)  # Initialize the login manager

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(main_blueprint)

    return app
