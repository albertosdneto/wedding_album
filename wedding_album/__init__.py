from flask import Flask


def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY='dev',
        debug=True,
    )

    from . import album
    app.register_blueprint(album.bp)
    app.add_url_rule('/', endpoint='index')

    return app
