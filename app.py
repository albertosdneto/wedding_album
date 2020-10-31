from flask import Flask
from . import album

app = Flask(__name__)

# @app.route('/')
# def hello_world():
#     return 'Hello World!'


app.register_blueprint(album.bp)
app.add_url_rule('/', endpoint='index')

if __name__ == '__main__':
    app.run()
