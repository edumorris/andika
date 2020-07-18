from flask import Flask
from config import config_options
from flask_bootstrap import Bootstrap

bootstrap = Bootstrap()


from flask import Blueprint
main = Blueprint('main', __name__)
from . import views, errors

def create_app(config_name):
    app = Flask(__name__)

    # Creating the app configurations
    app.config.from_object(config_options[config_name])

    # Initializing flak extensions
    bootstrap.init_app(app)

    # Registering the blueprint
    from ..main import main as main_blueprint # .main changed to ..main
    app.register_blueprint(main_blueprint)

    return app