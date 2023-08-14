from flask import Flask


def make_app():
    app = Flask(__name__)

    from .views import main_blueprint

    app.register_blueprint(main_blueprint)

    return app