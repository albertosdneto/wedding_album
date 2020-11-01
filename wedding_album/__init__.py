import os

from decouple import config
from flask import Flask
from mongoengine import connect
from werkzeug.security import generate_password_hash

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

    # Creates Admin on setup
    admin = User.objects(username='admin')
    if len(admin) == 0:
        new_admin = User(username='admin', password=generate_password_hash('admin'), role='host')
        new_admin.save()

    app.config.from_mapping(
        SECRET_KEY=secret_key,
        debug=debug,
    )

    from . import album
    app.register_blueprint(album.bp)
    app.add_url_rule('/', endpoint='index')

    from . import auth
    app.register_blueprint(auth.bp)

    return app
