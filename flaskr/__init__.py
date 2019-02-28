import os

from flask import Flask


def create_app(test_config = None):
    # create/configure the app

    # makes the instance of Flask, takes params __name__ (current python module we're in)
    # and the second one which tells the app that the config files are in the instance folder (outside of the flaskr package)
    app = Flask(__name__, instance_relative_config = True)

    # sets some default configs the app will use
    app.config.from_mapping(
        # helps keep data safe (how, Idunno)
        SECRET_KEY = 'dev',
        # where SQLite database file will be saved
        DATABASE = os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent = True)
    else:
        # load the test config if passed in (means we're testing)
        app.config.from_mapping(test_config)

    # enure the instance folder exists
    try:
        # creates app.instance_path if it doesn't already exist
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello World!'

    return app
