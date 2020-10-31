import os

from flask import Flask
from decouple import config
from mongoengine import connect
from .models import User


def create_app():
    app = Flask(__name__)
    is_prod = os.environ.get('IS_PROD', None)

    if is_prod:
        connect(host=os.environ.get('DATABASE_URL'))
        secret_key = os.environ.get('SECRET_KEY')
        debug = os.environ.get('DEBUG')
    else:
        connect(host=config('DATABASE_URL'))
        secret_key = config('SECRET_KEY')
        debug = config('DEBUG', default=False, cast=bool)

    app.config.from_mapping(
        SECRET_KEY=secret_key,
        debug=debug,
    )

    from . import album
    app.register_blueprint(album.bp)
    app.add_url_rule('/', endpoint='index')

    return app
