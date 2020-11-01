from mongoengine.document import Document
from mongoengine.fields import StringField


class User(Document):
    username = StringField(required=True, unique=True)
    password = StringField(required=True)
    role = StringField()

    meta = {
        'strict': False,
        'collection': 'users',
    }
