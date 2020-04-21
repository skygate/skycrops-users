from flask import Flask

from .routes import api

application = Flask(__name__)
application.register_blueprint(api)
