from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import Config

application = Flask(__name__)
application.secret_key = "super secret key"
application.config.from_object(Config)
db = SQLAlchemy(application)
migrate = Migrate(application, db)
login = LoginManager(application)


from .routes import api

application.register_blueprint(api)
